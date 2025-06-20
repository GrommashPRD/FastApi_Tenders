from fastapi import APIRouter

from app.api.handlers.organizations.create_organization import router as create_organization
from app.api.handlers.organizations.add_users_in_organization import router as add_users_in_organization

router = APIRouter(
    prefix="/organisation",
    tags=["Организации"]
)

router.include_router(create_organization)
router.include_router(add_users_in_organization)


