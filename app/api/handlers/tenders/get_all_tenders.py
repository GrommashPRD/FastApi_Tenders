from fastapi import HTTPException, APIRouter
from app.database import async_session_maker
from app.exceptions import TenderNotFound

from app.usecase.tenders import usecase

from app.logger import logger

router = APIRouter()

@router.get("/")
async def get_tenders():
    async with async_session_maker() as session:

        try:
            published_tenders = await usecase.get_published_tenders(session)
        except TenderNotFound:
            logger.warning("No published tenders were found.")
            raise HTTPException(status_code=404, detail="No published tenders were found.")

        return {
            "message": "OK",
            "tenders": published_tenders
        }
