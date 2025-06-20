from fastapi import Depends, HTTPException, APIRouter

from app.database import async_session_maker


from app.core.auth.dependencies import get_curr_user
from app.core.auth.models import User
from app.exceptions import BidNotFound
from app.usecase.bids import usecase

from app.logger import logger


router = APIRouter()

@router.get("/my/")
async def get_user_bids(user: User = Depends(get_curr_user)):
    async with async_session_maker() as session:

        try:
            bids = await usecase.get_all_bids_for_username(session, user.username)

        except BidNotFound:
            logger.warning("No bids found")
            raise HTTPException(detail="No bids found", status_code=404)

        return {
            "message": "OK",
            "bids": bids
        }
