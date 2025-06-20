from app.core.tenders.dao import TendersDAO
from app.core.tenders.models import TenderStatus


async def organizationResponsibleCount(session, tender_id):
    count = await TendersDAO.get_responsible_count(session, tender_id)
    return count


async def closeTheTender(session, tender_id: str):

    tender = await TendersDAO.find_by_id(
        id=tender_id
    )
    if tender:
        tender = tender
        tender.status = TenderStatus.CLOSED
        session.add(tender)
        await session.commit()
