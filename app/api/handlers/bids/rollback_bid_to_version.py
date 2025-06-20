from fastapi import Depends, HTTPException, APIRouter

from app.database import async_session_maker

from app.core.auth.dependencies import get_curr_user
from app.core.auth.models import User
from app.exceptions import BidNotFound, DontHavePermissions, VersionNotFound
from app.usecase.bids import usecase

from app.logger import logger


router = APIRouter()

@router.put("/{bid_id}/rollback/{version}")
async def bid_rollback(
        bid_id: str,
        version: int,
        user: User = Depends(get_curr_user),
):
    async with async_session_maker() as session:

        try:
            rollback = await usecase.rollback_bid_to_version(session, bid_id, version, user)

        except BidNotFound as e:
            logger.warning("Bid not found %s", e)
            raise HTTPException(detail="Bid not found", status_code=404)

        except DontHavePermissions as er:
            logger.warning("Dont have permissions %s", er)
            raise HTTPException(detail="Don't have permissions", status_code=403)

        except VersionNotFound as ve:
            logger.warning("Version not found %s", ve)
            raise HTTPException(detail="Version not found", status_code=404)

        return {
            "message": "OK",
            "tender_id": rollback.id,
            "new_name": rollback.name,
            "new_description": rollback.description,
            "version": rollback.version
        }