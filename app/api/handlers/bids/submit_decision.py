from fastapi import Depends, HTTPException

from app.database import async_session_maker
from app.core.bids.schemas import SBidDecision
from app.core.auth.dependencies import get_curr_user
from app.core.auth.models import User
from app.exceptions import BidNotFound, NonPublished, DecisionAlreadyExist
from app.usecase.bids import usecase
from app.logger import logger

from fastapi import APIRouter


router = APIRouter()

@router.put("/{bid_id}/submit_decision")
async def submit_decision(
        bid_id: str,
        status: SBidDecision,
        user: User = Depends(get_curr_user)
):
    async with async_session_maker() as session:

        try:
            decision = await usecase.submit_bid_decision(session, bid_id, user, status)

        except BidNotFound as e:
            logger.warning("Bid not found %s", e)
            raise HTTPException(detail="Bid not found", status_code=404)

        except NonPublished:
            logger.warning("Non-published")
            raise HTTPException(detail="Non-published bid", status_code=400)

        except DecisionAlreadyExist:
            logger.warning("Decision already exists")
            raise HTTPException(detail="You are already voted", status_code=400)

        return {
            "message": "OK",
            "decision": decision
        }
