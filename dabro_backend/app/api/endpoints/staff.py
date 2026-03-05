from fastapi import Depends, APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.models.staff_model import StaffModel

router = APIRouter(
    prefix="/staff",
    tags=["Staff"],
)


@router.get("/all")
async def get_all_staff(session: AsyncSession = Depends(get_db_session)):
    result = await session.execute(select(StaffModel).order_by(StaffModel.staff_id))
    staff = result.scalars().all()
    return staff
