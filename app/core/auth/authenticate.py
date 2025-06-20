from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from app.core.auth.dao import UsersDAO
from app.config import settings
from fastapi import HTTPException

from app.exceptions import UserNotFound, WrongPassword

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


async def authenticate_user(username: str, password: str):
    user = await UsersDAO.find_one_or_none(username=username)
    if not user:
        raise UserNotFound(status_code=401, detail=username)
    elif not verify_password(password, user.password):
        raise WrongPassword(status_code=401, detail="Incorrect password")

    return user