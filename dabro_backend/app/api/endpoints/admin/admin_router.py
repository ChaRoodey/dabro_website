from fastapi import APIRouter, Depends

from app.api.deps import require_auth
from app.api.endpoints.admin.products_edit import router as products_edit_router
from app.api.endpoints.admin.staff_edit import router as staff_edit_router
from app.api.endpoints.admin.auth import router as auth_router

router = APIRouter(
    prefix="/admin",
    # dependencies=[Depends(require_auth)]
)

router.include_router(staff_edit_router)
router.include_router(products_edit_router)
router.include_router(auth_router)
