from fastapi import APIRouter

from app.api.handlers.bids.create_new_bid import router as create_new_bid
from app.api.handlers.bids.get_all_bids_for_tender import router as get_all_bids_for_tender
from app.api.handlers.bids.get_bids_for_current_user import router as get_bids_for_current_user
from app.api.handlers.bids.get_or_update_bid_status import router as get_or_update_bid_status
from app.api.handlers.bids.get_reviews_about_bid import router as get_reviews_about_bid
from app.api.handlers.bids.rollback_bid_to_version import router as rollback_bid_to_version
from app.api.handlers.bids.submit_decision import router as submit_decision
from app.api.handlers.bids.submit_feedback import router as submit_feedback
from app.api.handlers.bids.update_bid_info import router as update_bid_info

router = APIRouter(
    prefix="/bids",
    tags=["Предложения"]
)

router.include_router(create_new_bid)
router.include_router(get_all_bids_for_tender)
router.include_router(get_bids_for_current_user)
router.include_router(get_or_update_bid_status)
router.include_router(get_reviews_about_bid)
router.include_router(rollback_bid_to_version)
router.include_router(submit_decision)
router.include_router(submit_feedback)
router.include_router(update_bid_info)