from app.core.bids.models import Bid, BidVersion, BidFeedback, BidDecisionModel
from sqlalchemy import select
from app.dao.base import BaseDAO
from app.database import async_session_maker


class BidsDAO(BaseDAO):
    model = Bid

    @classmethod
    async def bids_by_username(cls, session, username):
        query = select(cls.model).filter_by(creator_username=username)
        result = await session.execute(query)
        return result.mappings().all()

    @classmethod
    async def bid_by_user_for_tender(cls, session, tender_id, username):
        query = select(cls.model).filter_by(tender_id=tender_id, creator_username=username)
        result = await session.execute(query)
        return result.scalars().first()

    @classmethod
    async def bids_by_id(cls, session, id):
        query = select(cls.model).filter_by(id=id)
        result = await session.execute(query)
        return result.scalars().first()

    @classmethod
    async def find_bids_by_tender_id(
            cls,
            tender_id: str
    ):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(
                tender_id=tender_id
            )
            result = await session.execute(query)
            return result.mappings().all()

class BidVersionsDAO(BaseDAO):
    model = BidVersion

    @classmethod
    async def get_bid_version(
            cls,
            session,
            bid_id: str,
            version: int):
        result = await session.execute(
            select(cls.model).filter_by(
                bid_id=bid_id,
                version=version
            )
        )
        return result.scalars().first()

class BidsFeedBackDAO(BaseDAO):
    model = BidFeedback

    @classmethod
    async def get_bid_feedback(cls, session, bid_id: str, username: str):
        result = await session.execute(
            select(cls.model).filter(
                cls.model.feedback_by == username,
                cls.model.bid_id == bid_id
            )
        )
        return result.scalar()

    @classmethod
    async def get_reviews(
            cls,
            tender_id: str,
            author_username: str = None
    ):
        async with async_session_maker() as session:
            query = (
                select(BidFeedback)
                .join(Bid)
                .filter(Bid.tender_id == tender_id)
            )

            if author_username:
                query = query.filter(Bid.creator_username == author_username)

            result = await session.execute(query)
            feedbacks = result.scalars().all()

            feedback_list = [{"id": feedback.id,
                              "feedback": feedback.feedback,
                              "username": feedback.feedback_by}
                             for feedback in feedbacks]

            return feedback_list

class BidDecisionDAO(BaseDAO):
    model = BidDecisionModel

    @classmethod
    async def get_decision_by_user_and_bid(cls, session, user_id: str, bid_id: str):
        result = await session.execute(
            select(cls.model).filter(
                cls.model.user_id == user_id,
                cls.model.bid_id == bid_id
            )
        )

        return result.scalar()
