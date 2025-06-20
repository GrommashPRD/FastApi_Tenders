from fastapi import APIRouter

from app.api.handlers.tenders.create_new_tender import router as create_new_tender
from app.api.handlers.tenders.get_all_tenders import router as get_all_tenders
from app.api.handlers.tenders.get_or_update_tender_status import router as get_or_update_tender_status
from app.api.handlers.tenders.get_user_tenders import router as get_user_tenders
from app.api.handlers.tenders.rollback_tender import router as rollback_tender
from app.api.handlers.tenders.update_tender import router as update_tender

router = APIRouter(
    prefix="/tenders",
    tags=["Тендеры"]
)

router.include_router(create_new_tender)
router.include_router(get_all_tenders)
router.include_router(get_or_update_tender_status)
router.include_router(get_user_tenders)
router.include_router(rollback_tender)
router.include_router(update_tender)
