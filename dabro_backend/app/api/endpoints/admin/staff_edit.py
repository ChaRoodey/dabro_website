from typing import List
from uuid import uuid4
import json

from aiobotocore.client import AioBaseClient
from fastapi import Depends, APIRouter, HTTPException, UploadFile, File, Form, Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import op_context
from app.core.logging import get_logger
from app.db.session import get_transactional_session
from app.models.staff_model import StaffModel
from app.schemas.staff import StaffAddSchema, StaffPatchSchema, StaffDeleteSchema

from app.core.s3client import s3_client
from app.schemas.photo_meta import PhotoMetaSchema

from app.core.config import settings
from app.core.image_convert import convert_to_webp

router = APIRouter(
    prefix="/staff",
    tags=["Admin / Staff"],
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


@router.post("/add", dependencies=[Depends(op_context("staff.add"))])
async def add_staff(data: List[StaffAddSchema], session: AsyncSession = Depends(get_transactional_session)):
    new_rows = [StaffModel(**item.model_dump()) for item in data]
    session.add_all(new_rows)
    return {
        'status': 'ok',
        "created": len(new_rows)
    }


@router.patch("/change", dependencies=[Depends(op_context("staff.patch"))])
async def change_staff(data: List[StaffPatchSchema], session: AsyncSession = Depends(get_transactional_session)):
    ids = [item.staff_id for item in data]

    res = await session.execute(select(StaffModel).where(StaffModel.staff_id.in_(ids)))
    rows = res.scalars().all()
    by_id = {row.staff_id: row for row in rows}

    missing = [i for i in ids if i not in by_id]
    if missing:
        logger.warning("Missing staff ids:%s", missing)
        raise HTTPException(status_code=404, detail={"missing_staff_ids": missing})

    for item in data:
        staff = by_id[item.staff_id]
        update_data = item.model_dump(exclude_unset=True)
        update_data.pop("staff_id", None)
        for field, value in update_data.items():
            setattr(staff, field, value)
            logger.debug(f"Updated {field=}, {value=}")

    return {
        'status': 'ok',
        'updated': len(data)
    }


@router.delete("/delete", dependencies=[Depends(op_context("staff.delete"))])
async def delete_staff(data: StaffDeleteSchema, session: AsyncSession = Depends(get_transactional_session)):
    staff = await session.get(StaffModel, data.staff_id)
    if staff is None:
        logger.warning("Staff not found id=%s", data.staff_id)
        raise HTTPException(status_code=404, detail="Staff not found")

    await session.delete(staff)
    return {'status': 'ok'}

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
