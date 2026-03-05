from typing import List

from fastapi import Depends, APIRouter, UploadFile, File, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import op_context
from app.core.logging import get_logger
from app.core.xlsx_parser import parse_products_sheet
from app.db.session import get_transactional_session
from app.models.product_model import ProductModel
from app.schemas.product import ProductAddSchema, ProductPatchSchema, ProductDeleteSchema

router = APIRouter(
    prefix="/products",
    tags=["Admin / Products"],
)

logger = get_logger(__name__)


@router.post('/add', dependencies=[Depends(op_context("products.add"))])
async def add_product(data: List[ProductAddSchema], session: AsyncSession = Depends(get_transactional_session)):
    new_products = [ProductModel(**item.model_dump()) for item in data]
    session.add_all(new_products)
    return {
        'status': 'ok',
        "created": len(new_products)
    }


@router.patch("/change", dependencies=[Depends(op_context("products.change"))])
async def update_product(data: List[ProductPatchSchema], session: AsyncSession = Depends(get_transactional_session)):
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
async def delete_product(data: ProductDeleteSchema, session: AsyncSession = Depends(get_transactional_session)):
    product = await session.get(ProductModel, data.product_id)
    if product is None:
        logger.warning("Product not found id=%s", data.product_id)
        raise HTTPException(status_code=404, detail="Product not found")

    await session.delete(product)
    return {'status': 'ok'}


@router.post('/import', dependencies=[Depends(op_context("products.import_xlsx"))])
async def update_products_with_file(
        file: UploadFile = File(...),
        session: AsyncSession = Depends(get_transactional_session)
):
    if not file.filename.endswith('.xlsx'):
        logger.warning("Not .xlsx file filename: %s", file.filename)
        raise HTTPException(status_code=400, detail="Only .xlsx files are supported")

    raw = await file.read()
    try:
        rows = parse_products_sheet(raw)
    except Exception as e:
        logger.warning("Parsing error detail=%s", str(e))
        raise HTTPException(status_code=400, detail=str(e))

    if not rows:
        return {"status": "ok", "updated": 0, "skipped": 0, "missing": 0, "details": []}

    file_ids = [row['product_id'] for row in rows]

    res = await session.execute(
        select(ProductModel).where(ProductModel.product_id.in_(file_ids))
    )
    products = res.scalars().all()
    by_id = {p.product_id: p for p in products}

    updated = 0
    skipped = 0
    # missing = 0
    details = []

    for row in rows:
        product_id = row['product_id']
        obj = by_id.get(product_id)

        if obj is None:
            # missing += 1
            # details.append({"row": row["row"], "product_id": product_id, "action": "missing"})
            continue

        changed_fields = []

        if obj.cost != row['cost']:
            obj.cost = row['cost']
            changed_fields.append('cost')

        if obj.items_left != row['items_left']:
            obj.items_left = row['items_left']
            changed_fields.append('items_left')

        if changed_fields:
            updated += 1
            details.append(
                {"row": row["row"], "product_id": product_id, "action": "updated", "fields": changed_fields}
            )
        else:
            skipped += 1
            details.append({"row": row["row"], "product_id": product_id, "action": "no_changes"})

    return {
        "status": "ok",
        "updated": updated,
        "skipped": skipped,
        # "missing": missing,
        "details": details,
    }
