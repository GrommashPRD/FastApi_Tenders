from fastapi import Depends, HTTPException, APIRouter

from app.database import async_session_maker

from app.core.auth.dependencies import get_curr_user
from app.core.auth.models import User
from app.exceptions import TenderNotFound, DontHaveOrganization, DontHavePermissions, TenderNotfoundOrNotPublished
from app.usecase.bids import usecase

from app.logger import logger

router = APIRouter()


@router.get("/{tender_id}/list/")
async def get_bids_for_tender(
        tender_id: str,
        user: User = Depends(get_curr_user)
):
    async with async_session_maker():
        try:
            bids = await usecase.get_all_bids_for_tender(tender_id, user)

        except TenderNotFound:
            logger.warning("Tender not found")
            raise HTTPException(detail="Tender not found", status_code=404)

        except DontHaveOrganization:
            logger.warning("User dont have organization")
            raise HTTPException(detail="User dont have organization", status_code=404)

        except DontHavePermissions:
            logger.warning("User dont have permissions")
            raise HTTPException(detail="User dont have permissions", status_code=404)

        except TenderNotfoundOrNotPublished:
            logger.warning("Tender not found or not published", tender_id)
            raise HTTPException(detail="Tender not found or not published", status_code=404)


        return {
            "message": "OK",
            "tender": tender_id,
            "bids": bids
        }