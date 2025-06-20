from fastapi import Depends, HTTPException, APIRouter

from app.core.auth.dependencies import get_curr_user
from app.core.auth.models import User
from app.exceptions import OrganizationAlreadyExist, DatabaseError
from app.core.organizations.schemas import SOrganizationType, SOrganizationRequest
from app.database import async_session_maker
from app.usecase.addNewRecord import usecase

from app.logger import logger

router = APIRouter()

@router.post("/new/")
async def create_new(
        request: SOrganizationRequest,
        user: User = Depends(get_curr_user)
):
    if not request.name or request.name.strip() == "":
        logger.warning("Organization name is required")
        raise HTTPException(status_code=400, detail="Organization name is required")

    if request.org_type not in SOrganizationType._value2member_map_:
        logger.warning("Invalid organization type: %s", request.org_type)
        raise HTTPException(status_code=400, detail="Invalid organization type")

    async with async_session_maker() as session:
        try:
            organization = await usecase.create_organizations(session, request, user)
        except OrganizationAlreadyExist:
            logger.warning("Organization already exists")
            raise HTTPException(status_code=400, detail="Organization already exists")
        except DatabaseError:
            logger.warning("Database is unavailable. Please try again later.")
            raise HTTPException(status_code=503, detail="Database is unavailable")

    return {
        "message": "Organization created successfully",
        "organization_name": organization.name,
        "organization_id": organization.id
    }






