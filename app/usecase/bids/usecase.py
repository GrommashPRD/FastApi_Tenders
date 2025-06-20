from sqlalchemy.exc import SQLAlchemyError

from app.core.bids.dao import BidsDAO, BidsFeedBackDAO, BidVersionsDAO, BidDecisionDAO
from app.core.bids.models import BidStatus
from app.core.bids.schemas import SBidDecision, SBidCnceled, SBidStatus
from app.exceptions import *
from app.core.organizations.dao import OrganizationDAO
from app.core.tenders.models import TenderStatus
from app.utils import utils
from app.usecase.tenders import usecase


async def get_bid(bid_id, user):
    bid = await BidsDAO.find_by_id(
        id=bid_id
    )

    if not bid:
        raise BidNotFound(detail=bid_id, status_code=404)
    if bid.creator_username != user.username:
        raise DontHavePermissions(detail=user.id, status_code=403)

    return bid


async def get_all_bids_for_username(session, username):
    bids = await BidsDAO.bids_by_username(
        session,
        username
    )
    if not bids:
        raise BidNotFound("User dont have bids", status_code=404)
    return bids

async def get_all_bids_for_tender(tender_id, user):

    try:
        tender = await usecase.tenders_responsible(tender_id, user)

    except TenderNotFound:
        raise TenderNotFound("Tender not found", status_code=404)

    except UserNotResponsible:
        raise UserNotResponsible("User not responsible", status_code=404)

    if tender.status != TenderStatus.PUBLISHED:
        raise TenderNotfoundOrNotPublished("Tender not found or not published", tender.id)

    bids = await BidsDAO.find_bids_by_tender_id(
        tender_id=tender_id
    )
    return bids

async def get_reviews_for_bid(tender_id, author_username, user):

    try:
        await usecase.tenders_responsible(tender_id, user)

    except OrganizationNotFound:
        raise OrganizationNotFound("Organization not found", status_code=404)

    except TenderNotFound:
        raise TenderNotFound("Tender not found", status_code=404)

    except UserNotResponsible:
        raise UserNotResponsible("User not responsible", status_code=404)

    reviews = await BidsFeedBackDAO.get_reviews(tender_id, author_username)

    if not reviews:
        raise ReviewsNotFound(detail="Reviews not found", status_code=404)
    return reviews

async def rollback_bid_to_version(session, bid_id, version, user):
    bid = await get_bid(bid_id, user)

    bid_version = await BidVersionsDAO.get_bid_version(
        session,
        bid_id=bid.id,
        version=version,
    )
    if not bid_version:
        raise VersionNotFound(detail=version, status_code=404)

    bid.name = bid_version.name
    bid.description = bid_version.description

    session.add(bid)
    await session.commit()

    return bid

async def update_bid_status(session, bid_id, user, status):
    bid = await get_bid(bid_id, user)

    if bid.status != BidStatus.CREATED:
        raise ActionNotAllowed("Bid already published or closed", status_code=400)

    bid.status = status

    session.add(bid)
    await session.commit()

    return bid

async def submit_bid_decision(session, bid_id, user, status):
    bid = await get_bid(bid_id, user)

    if bid.status != BidStatus.PUBLISHED:
        raise NonPublished("Bid not published", status_code=400)

    decision = await BidDecisionDAO.get_decision_by_user_and_bid(
        session,
        user.id,
        bid.id,
    )

    if decision:
        raise DecisionAlreadyExist("Decision already exists", status_code=400)

    bid.status = status
    session.add(bid)

    new_decision = await BidDecisionDAO.add_new(
        session,
        user_id=user.id,
        bid_id=bid.id,
        status=status
    )

    session.add(new_decision)

    if status == SBidDecision.ACCEPTED:
        bid.votes += 1

    if status == SBidDecision.REJECTED:
        bid.status = SBidCnceled.CANCELED
        bid.votes = 0
        await session.commit()
        return {
            "message": "Bid rejected."
        }

    quorum = min(
        3,
        await utils.organizationResponsibleCount(session, bid.tender_id)
    )

    if bid.votes >= quorum:
        bid.status = SBidDecision.ACCEPTED
        await utils.closeTheTender(session, bid.tender_id)

    await session.commit()

    return quorum

async def submit_bid_feedback(session, bid_id, user, feedback):
    bid = await get_bid(bid_id, user)
    if bid.status != BidStatus.PUBLISHED:
        raise NonPublished("Bid not published", status_code=400)

    tender = await usecase.tenders_responsible(tender_id=bid.tender_id, user=user)

    organization = await OrganizationDAO.find_by_id(
        id=tender.organization_id
    )

    exist_feedback = await BidsFeedBackDAO.get_bid_feedback(
        session,
        bid_id,
        username=organization.name,
    )

    if exist_feedback:
        raise FeedbackAlreadyExist("You have already submitted for this bid.", status_code=400)

    try:
        feedback = await BidsFeedBackDAO.add_new(
            session,
            bid_id=bid.id,
            feedback=feedback.feedback,
            feedback_by=organization.name,
        )
        session.add(feedback)

    except SQLAlchemyError:
        raise DatabaseError(detail="Failure to create a new record", status_code=500)

    return feedback


async def update_bid_info(session, bid_id, update_data, user):
    bid = await get_bid(bid_id, user)

    if bid.status != BidStatus.CREATED:
        raise ActionNotAllowed("Bid already published or closed", status_code=400)

    try:
        new_version = await BidVersionsDAO.add_new(
            session,
            bid_id=bid.id,
            version=bid.version,
            name=bid.name,
            description=bid.description
        )
    except SQLAlchemyError:
        raise DatabaseError(detail="Failure to create a new record", status_code=500)

    bid.name = update_data.name
    bid.description = update_data.description
    bid.version += 1

    session.add(new_version)
    session.add(bid)
    await session.commit()

    return bid