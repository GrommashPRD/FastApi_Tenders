from fastapi import Depends, HTTPException, APIRouter
from app.database import async_session_maker

from app.core.auth.dependencies import get_curr_user
from app.core.auth.models import User
from app.exceptions import TenderNotFound, TenderNotfoundOrNotPublished, ActionNotAllowed
from app.usecase.tenders import usecase
from app.core.tenders.schemas import STenderStatus

from app.logger import logger

router = APIRouter()

@router.get("/{tender_id}/status/")
async def get_tender_status(
        tender_id: str,
        user: User = Depends(get_curr_user)
):
    async with async_session_maker():
        try:
            tender = await usecase.tender_status(tender_id, user)
        except TenderNotFound:
            logger.warning("Tender not found")
            raise HTTPException(status_code=404, detail="Tender not found")
        except TenderNotfoundOrNotPublished:
            logger.warning("Tender not found or not Published")
            raise HTTPException(status_code=404, detail="Tender not found or not Published")

        return {
            "message": "OK",
            "tender": tender_id,
            "status": tender.status.name,
        }


@router.put("/{tender_id}/status/")
async def update_tender_status(
        tender_id: str,
        status: STenderStatus,
        user: User = Depends(get_curr_user)
):
    async with async_session_maker() as session:
        try:
            tender = await usecase.update_tender_status(tender_id, user, status, session)
        except TenderNotFound:
            logger.warning("Tender not found")
            raise HTTPException(detail="Tender not found", status_code=404)
        except TenderNotfoundOrNotPublished:
            logger.warning("Tender not found or not Published")
            raise HTTPException(detail="Tender not found or not Published", status_code=404)
        except ActionNotAllowed:
            logger.warning("Action not allowed")
            raise HTTPException(detail="Tender is already published or closed", status_code=400)


        return {
            "message": "OK",
            "tender": tender.id,
            "new status": tender.status.name,
        }