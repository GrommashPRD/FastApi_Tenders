from fastapi import HTTPException, APIRouter
import re

from app.core.auth.schemas import SUserCreate
from app.database import async_session_maker
from sqlalchemy.exc import OperationalError
from app.exceptions import UserAlreadyExist
from app.usecase.auth import usecase

from app.logger import logger

router = APIRouter()

@router.post("/register/")
async def register_user(user_data: SUserCreate):
    if not user_data.username or not user_data.password:
        raise HTTPException(status_code=400, detail="Username and password are required")

    if not re.match(r'^[a-zA-Z0-9_]+$', user_data.username) or not re.match(r'^[a-zA-Z0-9!@#$%^&*().]+$', user_data.password):
        raise HTTPException(status_code=400,
                            detail="Username and password must contain only English letters, numbers, and underscores")

    async with async_session_maker() as session:
        try:
            registration = await usecase.register_user(session, user_data)
        except UserAlreadyExist:
            logger.warning("Username already registered")
            raise HTTPException(status_code=400, detail="Username already registered")
        except OperationalError:
            logger.warning("Database error")
            raise HTTPException(status_code=503, detail="Database error")

        return {
            "message": "OK",
            "user_id": registration.id
        }
