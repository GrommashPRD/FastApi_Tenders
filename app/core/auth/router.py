from fastapi import APIRouter

from app.api.handlers.auth.login import router as login_router
from app.api.handlers.auth.logout import router as logout_router
from app.api.handlers.auth.register import router as register_router

router = APIRouter(
    prefix="/auth",
    tags=["Авторизация"]
)

router.include_router(login_router)
router.include_router(register_router)
router.include_router(logout_router)