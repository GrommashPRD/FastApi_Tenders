from sqlalchemy.exc import SQLAlchemyError

from app.core.bids.dao import BidsDAO
from app.core.bids.models import BidStatus
from app.core.bids.schemas import SBidDecision
from app.exceptions import TenderNotFound, OrganizationNotFound, NonPublished, OrganizationAlreadyExist, \
    TenderAlreadyExist, UserNotResponsible, BidAlreadyExist, DatabaseError
from app.core.organizations.dao import OrgResponsibilityDAO, OrganizationDAO
from app.core.tenders.dao import TendersDAO


async def create_new_bid(session, bid, tender_id, is_from_organization, user):

    existing_bid = await BidsDAO.bid_by_user_for_tender(
        session,
        tender_id,
        username=user.username,
    )
    if existing_bid and existing_bid.status != SBidDecision.REJECTED:
        raise BidAlreadyExist("User already has a bid for this tender", status_code=400)

    tender = await TendersDAO.find_by_id(
        id=tender_id
    )
    if not tender:
        raise TenderNotFound("Tender not found", status_code=404)
    if tender.status.name != "PUBLISHED":
        raise NonPublished("Tender has not been published", status_code=404)

    org_responsible = await OrgResponsibilityDAO.find_organization_responsible(
        user_id=user.id
    )
    if not org_responsible and is_from_organization:
        raise OrganizationNotFound("You are dont have organization", status_code=404)

    organization_id = org_responsible.organization_id if is_from_organization else None

    try:
        new_bid = await BidsDAO.add_new(
            session,
            name=bid.name,
            description=bid.description,
            tender_id=tender_id,
            organization_id=organization_id,
            creator_username=user.username,
            status=BidStatus.CREATED,
        )
    except SQLAlchemyError:
        raise DatabaseError(detail="Failure to create a new record", status_code=500)

    return new_bid

async def create_organizations(session, request, user):

    existing_organization = await OrganizationDAO.find_by_name(
        session,
        name=request.name,
        username=user.username
    )
    if existing_organization:
        raise OrganizationAlreadyExist(detail="You already have an organization with that name", status_code=409)

    try:
        new_organization = await OrganizationDAO.add_new(
            session,
            name=request.name,
            description=request.description,
            organization_owner=user.username,
            type=request.org_type,
        )
    except SQLAlchemyError:
        raise DatabaseError(detail="Failure to create a new record", status_code=500)

    try:
        await OrgResponsibilityDAO.add_new(
            session,
            organization_id=new_organization.id,
            user_id=user.id,
        )
    except SQLAlchemyError:
        raise DatabaseError(detail="Failure to create a new record", status_code=500)

    return new_organization

async def create_new_tender(session, request, user):

    responsibility = await OrgResponsibilityDAO.find_organization_responsible(
        user_id=user.id
    )
    if not responsibility:
        raise UserNotResponsible("User not responsible for this organization.", status_code=403)

    existing_tender = await TendersDAO.find_existing_tender(
        session,
        title=request.title,
        organization_id=responsibility.organization_id
    )
    if existing_tender:
        raise TenderAlreadyExist("A tender with this title already exists.", status_code=400)

    try:
        new_tender = await TendersDAO.add_new(
            session,
            title=request.title,
            description=request.description,
            service_type=request.service_type,
            organization_id=responsibility.organization_id,
        )
    except SQLAlchemyError:
        raise DatabaseError(detail="Failure to create a new record", status_code=500)

    return new_tender
