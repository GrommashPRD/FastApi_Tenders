from fastapi import Response, APIRouter, HTTPException

from app.core.auth.schemas import SUserAuth
from app.core.auth.authenticate import authenticate_user, create_access_token
from app.exceptions import UserNotFound, WrongPassword
from app.logger import logger

router = APIRouter()

@router.post("/login/")
async def login_user(response: Response, user_data: SUserAuth):
    try:
        user = await authenticate_user(user_data.username, user_data.password)
    except UserNotFound as e:
        logger.warning("User not found %s", e)
        raise HTTPException(status_code=401, detail="User not found")
    except WrongPassword:
        logger.warning("Incorrect password")
        raise HTTPException(status_code=401, detail="Incorrect password")

    access_token = create_access_token({"sub": str(user.id)})

    response.set_cookie(
        "tenders_access_token",
        access_token,
        httponly=True,
    )

    return {
        "message": "OK",
        "user_id": user.id
    }