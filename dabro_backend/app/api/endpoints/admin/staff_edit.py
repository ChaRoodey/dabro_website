from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import op_context
from app.core.logging import get_logger
from app.db.session import get_transactional_session
from app.models.staff_model import StaffModel
from app.schemas.staff import StaffAddSchema, StaffPatchSchema, StaffDeleteSchema

router = APIRouter(
    prefix="/staff",
    tags=["Admin / Staff"],
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
async def add_staff(data: List[StaffPatchSchema], session: AsyncSession = Depends(get_transactional_session)):
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
