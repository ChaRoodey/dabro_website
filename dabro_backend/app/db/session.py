from typing import AsyncGenerator

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings
from app.core.logging import get_logger

engine = create_async_engine(settings.database_url, echo=False)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False)

logger = get_logger(__name__)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


async def get_transactional_session(
        request: Request,
        session: AsyncSession = Depends(get_db_session),
) -> AsyncGenerator[AsyncSession, None]:
    try:
        yield session
        await session.commit()

        op = getattr(request.state, "op", "unknown")

        logger.debug("Successful commit for %s path %s", op, request.url.path)
    except Exception:
        await session.rollback()
        logger.exception('DB transaction failed')
        raise
