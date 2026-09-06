import asyncio

from sqlalchemy import select

from app.core.config import settings
from app.core.logging import get_logger
from app.core.security import security
from app.db.session import SessionLocal
from app.models.user_model import UserModel

logger = get_logger(__name__)


async def ensure_initial_admin() -> None:
    username = settings.INITIAL_ADMIN_USERNAME
    password = settings.INITIAL_ADMIN_PASSWORD

    if not username or not password:
        logger.info("Initial admin credentials are not set, skipping admin bootstrap")
        return

    async with SessionLocal() as session:
        result = await session.execute(
            select(UserModel).where(UserModel.username == username)
        )
        existing_user = result.scalar_one_or_none()

        if existing_user:
            logger.info("Initial admin already exists: %s", username)
            return

        user = UserModel(
            username=username,
            password_hash=security.hash_password(password),
        )
        session.add(user)
        await session.commit()

        logger.info("Initial admin created: %s", username)


def main() -> None:
    asyncio.run(ensure_initial_admin())


if __name__ == "__main__":
    main()
