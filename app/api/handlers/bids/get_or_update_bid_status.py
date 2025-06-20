from fastapi import Depends, HTTPException, APIRouter

from app.database import async_session_maker

from app.core.bids.schemas import SBidStatus
from app.core.auth.dependencies import get_curr_user
from app.core.auth.models import User

from app.exceptions import BidNotFound, DontHavePermissions, ActionNotAllowed
from app.usecase.bids import usecase

from app.logger import logger


router = APIRouter()

@router.get("/{bid_id}/status/")
async def get_bid_status(
        bid_id: str,
        user: User = Depends(get_curr_user)
):
    async with async_session_maker():
        try:
            bid = await usecase.get_bid(bid_id, user)

        except BidNotFound as e:
            logger.warning("Bid not found %s", e)
            raise HTTPException(status_code=404, detail="Bid not found")

        except DontHavePermissions as e:
            logger.warning("User dont have permissions %s", e)
            raise HTTPException(status_code=403, detail="You dont have permissions")


        return {
            "Status": bid.status
        }

@router.put("/{bid_id}/status/")
async def update_bid_status(
        bid_id: str,
        status: SBidStatus,
        user: User = Depends(get_curr_user)
):
    async with async_session_maker() as session:

        try:
            bid = await usecase.update_bid_status(session, bid_id, user, status)
        except BidNotFound as e:
            logger.warning("Bid not found %s", e)
            raise HTTPException(detail="Bid not found",status_code=404)

        except DontHavePermissions as e:
            logger.warning("User dont have permissions %s", e)
            raise HTTPException(detail="User dont have permissions", status_code=403)

        except ActionNotAllowed:
            logger.warning("Bid already published or closed")
            raise HTTPException(detail="Bid already published or closed", status_code=404)

        return {
            "message": "OK",
            "id": bid.id,
            "status": bid.status
        }