import json
from pathlib import Path
from uuid import uuid4
from typing import List

from aiobotocore.client import AioBaseClient
from fastapi import Depends, APIRouter, UploadFile, File, HTTPException, Form
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import op_context
from app.core.config import settings
from app.core.image_convert import convert_to_webp
from app.core.logging import get_logger
from app.core.s3client import s3_client
from app.core.xlsx_parser import parse_products_sheet
from app.db.session import get_transactional_session
from app.models.product_model import ProductModel
from app.schemas.photo_meta import PhotoMetaSchema
from app.schemas.product import ProductAddSchema, ProductPatchSchema, ProductDeleteSchema

router = APIRouter(
    prefix="/products",
    tags=["Admin / Products"],
)

ALLOWED_EXTENSIONS = {".webp", ".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE = 10 * 1024 * 1024
FIELDS_TO_CHECK = (
    "cost",
    "items_left",
    "brand",
    "category",
    "description",
    "size",
    "title",
)

logger = get_logger(__name__)


@router.post('/add', dependencies=[Depends(op_context("products.add"))])
async def add_product(
        data: List[ProductAddSchema],
        session: AsyncSession = Depends(get_transactional_session)
):
    new_products = [ProductModel(**item.model_dump()) for item in data]
    session.add_all(new_products)
    return {
        'status': 'ok',
        "created": len(new_products)
    }


@router.patch("/change", dependencies=[Depends(op_context("products.change"))])
async def update_product(
        data: List[ProductPatchSchema],
        session: AsyncSession = Depends(get_transactional_session)
):
    ids = [item.product_id for item in data]

    res = await session.execute(select(ProductModel).where(ProductModel.product_id.in_(ids)))
    rows = res.scalars().all()
    by_id = {row.product_id: row for row in rows}

    missing = [i for i in ids if i not in by_id]
    if missing:
        logger.warning("Missing product ids:%s", missing)
        raise HTTPException(status_code=404, detail={"missing_products_ids": missing})

    for item in data:
        product = by_id[item.product_id]
        update_data = item.model_dump(exclude_unset=True)
        update_data.pop("staff_id", None)
        for field, value in update_data.items():
            setattr(product, field, value)

    return {
        'status': 'ok',
        'updated': len(data)
    }


@router.delete("/delete", dependencies=[Depends(op_context("products.delete"))])
async def delete_product(
        data: ProductDeleteSchema,
        session: AsyncSession = Depends(get_transactional_session)
):
    product = await session.get(ProductModel, data.product_id)
    if product is None:
        logger.warning("Product not found id=%s", data.product_id)
        raise HTTPException(status_code=404, detail="Product not found")

    await session.delete(product)
    return {'status': 'ok'}


@router.post('/upload-excel', dependencies=[Depends(op_context("products.upload-excel"))])
async def update_products_with_excel(
        file: UploadFile = File(...),
        session: AsyncSession = Depends(get_transactional_session)
):
    if not file.filename.endswith('.xlsx'):
        logger.warning("Not .xlsx file filename: %s", file.filename)
        raise HTTPException(status_code=400, detail={
            "status": "validation_error",
            "message": "Поддерживаются только файлы .xlsx",
        })

    raw = await file.read()
    try:
        parsed = parse_products_sheet(raw)
    except Exception as e:
        logger.warning("Parsing error detail=%s", str(e))
        raise HTTPException(status_code=400, detail={
            "status": "validation_error",
            "message": "Ошибка при чтении файла .xlsx",
        })

    rows = parsed['items']
    validation_errors = parsed["errors"]

    if validation_errors:
        return {
            "status": "validation_error",
            "message": "Файл содержит ошибки валидации",
            "errors": validation_errors,
        }

    if not rows:
        return {"status": "ok", "updated": 0, "skipped": 0, "details": []}

    file_ids = [row['excel_product_id'] for row in rows]

    res = await session.execute(
        select(ProductModel).where(ProductModel.excel_product_id.in_(file_ids))
    )
    products = res.scalars().all()
    by_id = {p.excel_product_id: p for p in products}

    added = 0
    updated = 0
    skipped = 0
    details = []

    for row in rows:
        excel_product_id = row["excel_product_id"]
        obj = by_id.get(excel_product_id)

        if obj is None:
            schema = ProductAddSchema(**row)
            session.add(ProductModel(**schema.model_dump()))
            added += 1
            details.append({
                "row": row["row"],
                "excel_id": excel_product_id,
                "action": "added",
            })
            continue

        changed_fields = []

        for field in FIELDS_TO_CHECK:
            new_value = row[field]
            old_value = getattr(obj, field)

            if old_value != new_value:
                setattr(obj, field, new_value)
                changed_fields.append(field)

        if changed_fields:
            updated += 1
            details.append({
                "row": row["row"],
                "excel_id": excel_product_id,
                "action": "updated",
                "fields": changed_fields,
            })
        else:
            skipped += 1
            details.append({
                "row": row["row"],
                "excel_id": excel_product_id,
                "action": "no_changes",
            })
    return {
        "status": "ok",
        'added': added,
        "updated": updated,
        "skipped": skipped,
        "details": details,
    }


@router.post('/upload-photos')
async def upload_photos(
        files: list[UploadFile] = File(...),
        meta: str = Form(...),
        s3_session: AioBaseClient = Depends(s3_client.get_client)
):
    try:
        meta_data = [PhotoMetaSchema(**item) for item in json.loads(meta)]
    except Exception:
        logger.warning("Invalid meta format: %s", json.loads(meta))
        raise HTTPException(status_code=400, detail="Invalid meta format")

    if len(meta_data) != len(files):
        logger.warning("Files and meta length mismatch. Meta: %s, Files: %s.", len(meta_data), len(files))
        raise HTTPException(status_code=400, detail="Files and meta length mismatch")

    uploaded_files = []

    for item in meta_data:
        if item.index >= len(files):
            logger.warning("Invalid file index: %s. File len: %s", item.index, len(files))
            raise HTTPException(400, "Invalid file index")

        file = files[item.index]

        ext = Path(file.filename).suffix.lower()

        if ext not in ALLOWED_EXTENSIONS:
            logger.warning("Unsupported file extension: %s", file.filename)
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}")

        if not file.content_type or not file.content_type.startswith("image/"):
            logger.warning("File must be an image %s", file.filename)
            raise HTTPException(400, "File must be an image")

        content = await file.read()
        if not content:
            logger.warning("Empty file: %s", file.filename)
            raise HTTPException(400, "Empty file")

        if len(content) > MAX_FILE_SIZE:
            logger.warning("File too large (max 10MB). Curr size: %s", len(content))
            raise HTTPException(status_code=413, detail="File too large (max 10MB)")

        try:
            content_webp = convert_to_webp(content)
        except ValueError:
            logger.exception("Image resolution too large, file: %s", file.filename)
            raise HTTPException(400, "Image resolution too large")
        except Exception:
            logger.exception("Image conversion failed: %s", file.filename)
            raise HTTPException(400, "Invalid image file")

        image_name = f"{uuid4()}.webp"

        try:
            await s3_client.upload_file(s3_session, content_webp, image_name)
        except Exception as e:
            logger.exception("Uploading photo failed: %s", str(e))
            raise HTTPException(500, "Failed to upload file")

        uploaded_files.append({
            'id': item.id,
            'img_url': f'{settings.S3_GET_URL}{image_name}',
        })

    logger.debug("Successfully added %s photos: %s", len(uploaded_files), uploaded_files)

    return {
        'status': 'ok',
        'files': uploaded_files,
    }
