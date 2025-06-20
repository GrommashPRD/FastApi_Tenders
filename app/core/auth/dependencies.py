from fastapi import Request, HTTPException, Depends
from jose import jwt, JWTError
from app.config import settings
from datetime import datetime

from app.core.auth.dao import UsersDAO


def get_token(request: Request):
    token = request.cookies.get('tenders_access_token')
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token")
    return token

async def get_curr_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token,
            key=settings.SECRET_KEY,
            algorithms=settings.ALGORITHM
        )
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    expire: str = payload.get('exp')
    if not expire or (int(expire) < datetime.utcnow().timestamp()):
        raise HTTPException(status_code=401, detail="Invalid token")
    user_id: str = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = await UsersDAO.find_by_id(str(user_id))
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user

