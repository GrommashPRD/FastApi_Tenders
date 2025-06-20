from fastapi import Depends, HTTPException, APIRouter
from app.database import async_session_maker
from sqlalchemy.exc import DataError, OperationalError

from app.core.auth.dependencies import get_curr_user
from app.core.auth.models import User
from app.exceptions import TenderNotFound, UserNotResponsible

from app.core.tenders.schemas import SUpdateTenderDescription
from app.usecase.tenders import usecase

from app.logger import logger

router = APIRouter()

@router.patch("/{tender_id}/edit")
async def update_tender(
        tender_id: str,
        update_data: SUpdateTenderDescription,
        user: User = Depends(get_curr_user)
):
    async with async_session_maker() as session:
        try:
            tender = await usecase.update_tender_info(session, tender_id, update_data, user)
        except TenderNotFound:
            logger.warning("Tender not found")
            raise HTTPException(status_code=404, detail="Tender not found")
        except UserNotResponsible:
            logger.warning("User not responsible")
            raise HTTPException(status_code=404, detail="User not responsible")
        except DataError:
            logger.warning("Data error")
            raise HTTPException(status_code=404, detail="Data error")
        except OperationalError:
            logger.warning("Operational error")
            raise HTTPException(status_code=404, detail="Operational error")

        return {
            "message": "OK",
            "tender_id": tender.id,
            "new_description": tender.description,
            "version": tender.version
        }

