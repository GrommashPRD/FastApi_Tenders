from fastapi import Depends, HTTPException, APIRouter

from app.database import async_session_maker

from app.core.bids.schemas import SBidCreate

from app.core.auth.dependencies import get_curr_user
from app.core.auth.models import User
from app.exceptions import TenderNotFound, NonPublished, OrganizationNotFound, BidAlreadyExist, DatabaseError

from app.usecase.addNewRecord import usecase

from app.logger import logger

router = APIRouter()

@router.post("/new/")
async def create_bid(bid: SBidCreate,
                     tender_id: str,
                     is_from_organization: bool,
                     user: User = Depends(get_curr_user)
):
    async with async_session_maker() as session:

        try:
            bid = await usecase.create_new_bid(session, bid, tender_id, is_from_organization, user)

        except TenderNotFound as tnf:
            logger.warning("tender not found %s", tnf)
            raise HTTPException(status_code=404, detail="Tender not found")

        except NonPublished as np:
            logger.warning("Non-published tender %s", np)
            raise HTTPException(status_code=404, detail="Tender is non-published")

        except OrganizationNotFound as onf:
            logger.warning("User dont have organization %s", onf)
            raise HTTPException(status_code=404, detail="You are dont have organization")

        except BidAlreadyExist:
            logger.warning("Bid already exist %s", bid)
            raise HTTPException(status_code=404, detail="You are already have a bid for this tender")

        except DatabaseError:
            logger.warning("Database error %s", DatabaseError)
            raise HTTPException(status_code=500, detail="Failure to create a new record")


        return {
            "message": "OK",
            "id": bid.id,
            "status": bid.status,
        }