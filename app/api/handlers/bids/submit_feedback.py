from fastapi import Depends, HTTPException

from app.database import async_session_maker


from app.core.bids.schemas import SBidFeedback

from app.core.auth.dependencies import get_curr_user
from app.core.auth.models import User
from app.exceptions import BidNotFound, DontHavePermissions, FeedbackAlreadyExist, NonPublished

from app.usecase.bids import usecase

from app.logger import logger
from fastapi import APIRouter

router = APIRouter()

@router.put("/{bid_id}/feedback/")
async def submit_feedback(
        bid_id: str,
        feedback: SBidFeedback,
        user: User = Depends(get_curr_user),
):
    async with async_session_maker() as session:

        try:
            feedback = await usecase.submit_bid_feedback(session, bid_id, user, feedback)
        except BidNotFound as e:
            logger.warning("Bid not found %s", e)
            raise HTTPException(detail="Bid not found", status_code=404)

        except DontHavePermissions:
            logger.warning("You don't have the rights for this action.")
            raise HTTPException(detail="You don't have the rights for this action", status_code=403)

        except FeedbackAlreadyExist:
            logger.warning("You have already submitted for this bid.")
            raise HTTPException(detail="You have already submitted for this bid.", status_code=404)

        except NonPublished:
            logger.warning("Bid not published or not found")
            raise HTTPException(detail="Bid not published or not found", status_code=404)

        return {
            "message": "OK",
            "feedback": feedback
        }