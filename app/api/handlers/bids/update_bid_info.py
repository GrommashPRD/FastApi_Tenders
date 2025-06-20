from fastapi import Depends, HTTPException

from app.database import async_session_maker

from app.core.bids.schemas import SBidUpdate

from app.core.auth.dependencies import get_curr_user
from app.core.auth.models import User
from app.exceptions import BidNotFound, DontHavePermissions, ActionNotAllowed
from app.usecase.bids import usecase

from app.logger import logger
from fastapi import APIRouter

router = APIRouter()

@router.patch("/{bid_id}/edit", operation_id="update_bid")
async def update_bid(
        bid_id: str,
        update_data: SBidUpdate,
        user: User = Depends(get_curr_user),
):
    async with async_session_maker() as session:

        try:
            bid = await usecase.update_bid_info(session, bid_id, update_data, user)

        except BidNotFound as e:
            logger.warning("Bid not found %s", e)
            raise HTTPException(detail="Bid not found", status_code=404)

        except DontHavePermissions:
            logger.warning("You don't have the rights for this action.")
            raise HTTPException(detail="You don't have the rights for this action", status_code=403)

        except ActionNotAllowed:
            logger.warning("Can not update bid")
            raise HTTPException(detail="Can not update bid", status_code=400)

        return {
            "message": "OK",
            "tender_id": bid.id,
            "new_description": bid.description,
            "version": bid.version
        }