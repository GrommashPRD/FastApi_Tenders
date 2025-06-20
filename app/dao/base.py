from app.database import async_session_maker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select

from app.exceptions import DatabaseError


class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, id: str):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=id)
            result = await session.execute(query)
            return result.scalars().first()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls):
        async with async_session_maker() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.mappings().all()


    @classmethod
    async def add_new(cls, session, **data):
        new_instance = cls.model(**data)
        session.add(new_instance)

        try:
            await session.commit()
            return new_instance
        except SQLAlchemyError as err:
            await session.rollback()
            raise DatabaseError("An error occurred while adding a new instance.", status_code=500) from err
