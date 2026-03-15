from fastapi import Depends, HTTPException, Response, Request, APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_auth
from app.core.config import settings
from app.core.logging import get_logger
from app.core.security import security
from app.core.session import create_session, delete_session
from app.db.session import get_transactional_session
from app.models.session_model import SessionModel
from app.models.user_model import UserModel
from app.schemas.admin import LoginSchema

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)
logger = get_logger(__name__)


def _set_session_cookie(response: Response, token: str):
    response.set_cookie(
        key=settings.SESSION_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=settings.SESSION_COOKIE_SECURE,
        samesite="lax",
        max_age=settings.SESSION_TTL_HOURS * 3600,
        domain=settings.SESSION_COOKIE_DOMAIN,
    )


@router.post("/login")
async def login(
        data: LoginSchema,
        response: Response,
        session: AsyncSession = Depends(get_transactional_session)
):
    logger.info("Login attempt username=%s", data.username)
    try:
        res = await session.execute(select(UserModel).filter_by(username=data.username))
        user = res.scalars().one_or_none()
    except Exception:
        logger.exception("Login failed: DB error username=%s", data.username)
        raise

    if not user:
        logger.warning("Login failed: user not found username=%s", data.username)
        raise HTTPException(status_code=401, detail="Неправильный логин или пароль")

    if not security.verify_password(data.password, user.password_hash):
        logger.warning("Login failed: wrong password username=%s", data.username)
        raise HTTPException(status_code=401, detail="Неправильный логин или пароль")

    session_obj = await create_session(user.user_id, session)

    _set_session_cookie(response, str(session_obj.session_id))

    return {"success": True}


@router.post("/logout")
async def logout(
        request: Request,
        response: Response,
        session: AsyncSession = Depends(get_transactional_session)
):
    session_id = request.cookies.get(settings.SESSION_COOKIE_NAME)
    if session_id:
        res = await session.execute(select(SessionModel).filter_by(session_id=session_id))
        session_obj = res.scalar_one_or_none()
        if session_obj:
            await delete_session(session_obj.session_id, session)

    response.delete_cookie(settings.SESSION_COOKIE_NAME)
    return {"success": True}


@router.get("/check")
async def check_login(_=Depends(require_auth)) -> dict:
    return {"success": True}


# @router.post("/registration")
# async def registration(
#         data: LoginSchema,
#         session: AsyncSession = Depends(get_transactional_session)
# ) -> dict:
#     new_user = UserModel(username=data.username, password_hash=security.hash_password(data.password))
#     session.add(new_user)
#     return {"success": True}
