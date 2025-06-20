from fastapi import HTTPException
from app.dao.base import BaseDAO
from app.database import async_session_maker
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.core.organizations.models import Organization, OrganizationResponsible


class OrganizationDAO(BaseDAO):
    model = Organization

    @classmethod
    async def find_by_name(cls, session, name: str, username: str):
        query = select(
            cls.model
        ).filter_by(
            name=name,
            organization_owner=username
        )
        result = await session.execute(query)
        return result.scalars().first()


class OrgResponsibilityDAO(BaseDAO):
    model = OrganizationResponsible

    @classmethod
    async def add_users_to_organization(
            cls,
            session,
            organization_id: str,
            user_ids: list
    ):
        existing_users = await session.execute(
            select(
                cls.model.user_id
            )
            .filter(
                cls.model.organization_id == organization_id, cls.model.user_id.in_(user_ids)
            )
        )

        existing_user_ids = {user_id for (user_id,) in existing_users.fetchall()}

        responsibilities = [
            cls.model(
                organization_id=organization_id,
                user_id=user_id
            )
            for user_id in user_ids
            if user_id not in existing_user_ids
        ]

        if responsibilities:
            try:
                session.add_all(responsibilities)
                await session.commit()
            except IntegrityError as e:
                await session.rollback()
                raise HTTPException(detail=f"Ошибка добавления пользователей: {str(e)}", status_code=400)

        return existing_user_ids

    @classmethod
    async def find_org_by_user_id(cls, usr_id: str):
        async with async_session_maker() as session:
            query = select(
                cls.model
            ).filter_by(
                user_id=usr_id
            )
            result = await session.execute(query)
            return result.scalars().first()

    @classmethod
    async def find_organization_responsible(cls, user_id: str):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(user_id=user_id)
            result = await session.execute(query)
            return result.scalars().first()

