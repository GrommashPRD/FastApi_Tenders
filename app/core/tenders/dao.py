from app.dao.base import BaseDAO
from sqlalchemy import select, func

from app.database import async_session_maker
from app.core.organizations.models import OrganizationResponsible
from app.core.tenders.models import Tender, TenderVersion, TenderStatus


class TendersDAO(BaseDAO):
    model = Tender

    @classmethod
    async def get_by_status(
            cls,
            session,
            status_value
    ):
        query = select(
            cls.model
        ).filter_by(
            status=status_value
        )
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def find_by_organization_id(cls, session, username):
        query = select(cls.model).filter_by(organization_id=username)
        result = await session.execute(query)
        return result.mappings().all()

    @classmethod
    async def find_existing_tender(cls, session, title: str, organization_id: int):
        query = await session.execute(
            select(cls.model).where(
                cls.model.title == title,
                cls.model.organization_id == organization_id
            )
        )
        return query.scalars().first()

    @classmethod
    async def get_responsible_count(cls, session, tender_id: str):
        tender = await session.execute(
            select(Tender.organization_id).filter(Tender.id == tender_id)
        )
        organization_id = tender.scalar()

        if organization_id is None:
            return 0

        result = await session.execute(
            select(func.count()).filter(OrganizationResponsible.organization_id == organization_id)
        )

        return result.scalar()

    @classmethod
    async def close_tender(cls, tender_id: str):
        async with async_session_maker() as session:
            tender = await session.execute(
                select(Tender).filter(Tender.id == tender_id)
            )
            if tender:
                tender = tender.scalar()
                tender.status = TenderStatus.CLOSED
                session.add(tender)
                await session.commit()

class TendersVersionsDAO(BaseDAO):
    model = TenderVersion

    @classmethod
    async def get_tender_version(cls, session, tender_id: str, version: int):
        result = await session.execute(
            select(cls.model).filter_by(tender_id=tender_id, version=version)
        )
        return result.scalars().first()