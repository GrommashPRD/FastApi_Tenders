from fastapi import Depends, HTTPException, APIRouter
from app.database import async_session_maker

from app.core.auth.dependencies import get_curr_user
from app.core.auth.models import User
from app.exceptions import UserNotResponsible, TenderAlreadyExist, DatabaseError

from app.core.tenders.schemas import STenderCreateRequest

from app.logger import logger
from app.usecase.addNewRecord import usecase

router = APIRouter()

@router.post("/new/")
async def create_new_tender(
        request: STenderCreateRequest,
        user: User = Depends(get_curr_user),
):
    async with async_session_maker() as session:

        try:
            tender = await usecase.create_new_tender(session, request, user)
        except UserNotResponsible:
            logger.warning("User not responsible")
            raise HTTPException(status_code=403, detail="You are not responsible to create new tender.")
        except TenderAlreadyExist:
            logger.warning("Tender already exists")
            raise HTTPException(status_code=400, detail="Tender already exists.")
        except DatabaseError:
            logger.warning("Database error")
            raise HTTPException(status_code=500, detail="Database error.")

        return tender


