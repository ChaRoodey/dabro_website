from fastapi import Depends, APIRouter
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.models.product_model import ProductModel
from app.schemas.filters import FiltersSchema, filters_query

router = APIRouter(
    prefix="/products",
    tags=["Products"],
)


@router.get("/all")
async def get_all_products(session: AsyncSession = Depends(get_db_session)):
    result = await session.execute(select(ProductModel))
    products = result.scalars().all()
    return products


@router.get("/filters")
async def get_all_filters(session: AsyncSession = Depends(get_db_session)):
    brands_res = await session.execute(
        select(ProductModel.brand).distinct()
    )
    categories_res = await session.execute(
        select(ProductModel.category).distinct()
    )
    prices_res = await session.execute(
        select(func.min(ProductModel.cost), func.max(ProductModel.cost))
    )
    min_price, max_price = prices_res.one()
    return {
        "brands": brands_res.scalars().all(),
        "categories": categories_res.scalars().all(),
        "min_price": min_price,
        "max_price": max_price,
    }


@router.get("/filter")
async def get_products_by_filter(
        filters: FiltersSchema = Depends(filters_query),
        session: AsyncSession = Depends(get_db_session),
):
    stmt = select(ProductModel)

    conditions = [
        ProductModel.brand.in_(filters.brands) if filters.brands else None,
        ProductModel.category.in_(filters.categories) if filters.categories else None,
        ProductModel.cost >= filters.min_price if filters.min_price is not None else None,
        ProductModel.cost <= filters.max_price if filters.max_price is not None else None,
    ]

    stmt = stmt.where(*[c for c in conditions if c is not None])

    result = await session.execute(stmt)
    products = result.scalars().all()
    return products
