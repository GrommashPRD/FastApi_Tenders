from fastapi import Depends, HTTPException, APIRouter

from app.core.auth.dependencies import get_curr_user
from app.core.auth.models import User
from app.exceptions import UserAlreadyInOrganization, OrganizationNotFound, UserNotResponsible, DatabaseError
from app.database import async_session_maker
from app.usecase.organizations import usecase

from app.logger import logger

router = APIRouter()

@router.post("/{organization_id}/add_users/")
async def add_users_to_organization(
    organization_id: str,
    user_ids: list[str],
    user: User = Depends(get_curr_user),
):
    async with (async_session_maker() as session):
        try:
            await usecase.add_responsible_users(session, organization_id, user_ids, user)
        except OrganizationNotFound:
            logger.warning("Organization not found")
            raise HTTPException(status_code=404, detail="Organization not found")
        except UserNotResponsible:
            logger.warning("User not responsible to adding users")
            raise HTTPException(status_code=404, detail="You are not responsible to adding users")
        except UserAlreadyInOrganization:
            logger.warning("User already in organization")
            raise HTTPException(status_code=404, detail="User already in organization")
        except DatabaseError:
            logger.warning("Database is unavailable. Please try again later.")
            raise HTTPException(status_code=503, detail="Database is unavailable")

    return {
        "message": "OK",
    }