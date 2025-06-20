from fastapi import Depends, APIRouter
from app.database import async_session_maker

from app.core.auth.dependencies import get_curr_user
from app.core.auth.models import User
from app.exceptions import TenderNotFound

from app.usecase.tenders import usecase

from app.logger import logger

router = APIRouter()

@router.get("/my/")
async def get_my_tenders(
        user: User = Depends(get_curr_user)
):
    async with async_session_maker() as session:
        tenders = await usecase.get_users_tenders(session, user)
        if not tenders:
            logger.warning("There are no tenders")
            raise TenderNotFound(status_code=404, detail="You don't have any tenders")

        return {
            "message": "OK",
            "tenders": tenders
        }