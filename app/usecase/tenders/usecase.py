from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.exceptions import TenderNotFound, TenderNotfoundOrNotPublished, UserNotResponsible, VersionNotFound, \
    TendersNotExist, DatabaseError, OrganizationNotFound, ActionNotAllowed
from app.core.organizations.dao import OrgResponsibilityDAO
from app.core.tenders.dao import TendersDAO, TendersVersionsDAO
from app.core.tenders.models import TenderStatus


async def get_tender(tender_id):
    tender = await TendersDAO.find_by_id(
        id=tender_id
    )
    if not tender:
        raise TenderNotFound("Tender not found", status_code=404)

    return tender

async def get_published_tenders(session):
    published_tenders = await TendersDAO.get_by_status(session, TenderStatus.PUBLISHED)

    if not published_tenders:
        raise TendersNotExist("No published tenders were found.", status_code=404)

    return published_tenders

async def tenders_responsible(tender_id, user):
    try:
        tender = await get_tender(tender_id)
    except TenderNotFound:
        raise TenderNotFound("Tender not found", status_code=404)

    organization_by_user = await OrgResponsibilityDAO.find_organization_responsible(user_id=user.id)

    if not organization_by_user:
        raise OrganizationNotFound("Organization responsible not found", status_code=404)

    if organization_by_user.organization_id != tender.organization_id:
        raise UserNotResponsible("You are not responsible for this organization.", status_code=403)

    return tender

async def get_users_tenders(session, user):

    organization_by_user = await OrgResponsibilityDAO.find_organization_responsible(user_id=user.id)

    if not organization_by_user:
        raise UserNotResponsible("You are not responsible for this organization", status_code=403)

    tenders = await TendersDAO.find_by_organization_id(session, organization_by_user.organization_id)

    if not tenders:
        raise TenderNotFound(detail="You don't have any tenders", status_code=404)

    return tenders

async def tender_status(tender_id, user):

    try:
        tender = await get_tender(tender_id)
    except TenderNotFound:
        raise TenderNotFound("Tender not found", status_code=404)

    organization_by_user = await OrgResponsibilityDAO.find_organization_responsible(user_id=user.id)

    if organization_by_user:
        if organization_by_user.organization_id != tender.organization_id and tender.status != TenderStatus.PUBLISHED:
            raise TenderNotfoundOrNotPublished("Tender not found or not PUBLISHED", status_code=403)
        return tender

    if tender.status == TenderStatus.CREATED:
        raise TenderNotfoundOrNotPublished("Tender not found or not PUBLISHED", status_code=403)

    return tender


async def update_tender_status(tender_id, user, status, session):
    try:
        tender = await tenders_responsible(tender_id, user)
    except TenderNotFound:
        raise TenderNotFound("Tender not found", status_code=404)
    except OrganizationNotFound:
        raise OrganizationNotFound("Organization responsible not found", status_code=404)
    except UserNotResponsible:
        raise UserNotResponsible("You are not responsible for this tender.", status_code=403)

    if tender.status != TenderStatus.CREATED:
        raise ActionNotAllowed("Tender is already published or closed", status_code=400)

    tender.status = status
    session.add(tender)
    await session.commit()

    return tender


async def rollback_to_version(session, tender_id, user, version):

    tender = await tenders_responsible(tender_id, user)

    tender_version = await TendersVersionsDAO.get_tender_version(
        session,
        tender_id=tender_id,
        version=version
    )
    if not tender_version:
        raise VersionNotFound("Version not found", status_code=404)

    try:
        new_version = await TendersVersionsDAO.add_new(
            session,
            tender_id=tender.id,
            version=tender.version,
            description=tender.description,
        )

    except SQLAlchemyError:
        raise DatabaseError(detail="Failure to create a new record", status_code=500)

    tender.description = tender_version.description
    tender.version += 1
    session.add(new_version)
    session.add(tender)
    await session.commit()

    return tender

async def update_tender_info(session, tender_id, update_data, user):

    tender = await tenders_responsible(tender_id, user)

    if update_data.description is None or update_data.description.strip() == "":
        raise HTTPException(detail="Description cannot be empty", status_code=400)

    try:
        new_version = await TendersVersionsDAO.add_new(
            session,
            tender_id=tender.id,
            version=tender.version,
            description=tender.description,
        )
    except SQLAlchemyError:
        raise DatabaseError(detail="Failure to create a new record", status_code=500)

    tender.description = update_data.description
    tender.version += 1

    session.add(new_version)
    session.add(tender)
    await session.commit()

    return tender