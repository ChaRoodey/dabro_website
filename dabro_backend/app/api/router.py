from fastapi import APIRouter

from app.api.endpoints.products import router as products_router
from app.api.endpoints.staff import router as staff_router
from app.api.endpoints.admin.admin_router import router as admin_router
from app.api.endpoints.admin.auth import router as auth_router

router = APIRouter()
router.include_router(products_router)
router.include_router(staff_router)
router.include_router(admin_router)
router.include_router(auth_router)
