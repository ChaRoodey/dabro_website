import uuid
from datetime import datetime, timezone

from fastapi import Depends, Request, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import get_logger
from app.core.session import get_session
from app.db.session import get_db_session


logger = get_logger(__name__)


async def require_auth(
        request: Request,
        session: AsyncSession = Depends(get_db_session),
):
    session_id = request.cookies.get('session_id')

    if not session_id:
        logger.warning("Not authenticated")
        raise HTTPException(status_code=401, detail='Not authenticated')

    try:
        session_uuid = uuid.UUID(session_id)
    except ValueError:
        logger.warning("Invalid session id:%s", session_id)
        raise HTTPException(status_code=401, detail='Invalid session id')

    session_obj = await get_session(session_uuid, session)

    if not session_obj:
        logger.warning("Session not found for id:%s", session_uuid)
        raise HTTPException(status_code=401, detail='Session not found')

    if session_obj.expires_at < datetime.now(timezone.utc):
        logger.warning("Session expired id:%s", session_uuid)
        raise HTTPException(status_code=401, detail='Session expired')

    return session_obj.user_id


def op_context(op: str):
    async def _dep(request: Request):
        request.state.op = op

    return _dep
