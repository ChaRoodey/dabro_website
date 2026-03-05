from fastapi import Depends, HTTPException, Response, Request, APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import require_auth
from app.core.config import settings
from app.core.security import security
from app.core.session import create_session, delete_session
from app.db.session import get_db_session
from app.models.session_model import SessionModel
from app.models.user_model import UserModel
from app.schemas.admin import LoginSchema

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


def _set_session_cookie(response: Response, token: str):
    response.set_cookie(
        key=settings.SESSION_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=settings.SESSION_COOKIE_SECURE,
        samesite="lax",
        max_age=settings.SESSION_TTL_HOURS * 360,
        domain=settings.SESSION_COOKIE_DOMAIN,
    )


@router.post("/login")
async def login(
        data: LoginSchema,
        response: Response,
        session: AsyncSession = Depends(get_db_session)
):
    res = await session.execute(select(UserModel).filter_by(username=data.username))
    user = res.scalars().one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    if not security.verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Wrong Password")

    session_obj = await create_session(user.user_id, session)

    _set_session_cookie(response, str(session_obj.session_id))

    return {"success": True}


@router.post("/logout")
async def logout(
        request: Request,
        response: Response,
        session: AsyncSession = Depends(get_db_session)
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
async def check_login(user_id: int = Depends(require_auth)) -> dict:
    return {"success": True}


@router.post("/registration")
async def registration(
        data: LoginSchema,
        session: AsyncSession = Depends(get_db_session)
) -> dict:
    new_user = UserModel(username=data.username, password_hash=security.hash_password(data.password))
    session.add(new_user)
    await session.commit()
    return {"success": True}
