from sqlalchemy.exc import SQLAlchemyError

from app.core.auth.authenticate import hash_password
from app.core.auth.dao import UsersDAO
from app.exceptions import UserAlreadyExist, DatabaseAddingError, DatabaseError


async def register_user(session, user_data):

    existing_user = await UsersDAO.find_one_or_none(username=user_data.username)
    if existing_user:
        raise UserAlreadyExist(status_code=400, detail="Username already registered")

    hashed_password = hash_password(user_data.password)

    try:
        new_user = await UsersDAO.add_new(
            session,
            username=user_data.username,
            password=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
    except SQLAlchemyError:
        raise DatabaseError(detail="Database error", status_code=500)

    if not new_user:
        await session.rollback()
        raise DatabaseAddingError(status_code=503, detail="Database is unavailable. Please try again later.")

    return new_user