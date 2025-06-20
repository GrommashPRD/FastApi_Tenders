from fastapi import Depends, HTTPException, APIRouter
from app.database import async_session_maker

from app.core.auth.dependencies import get_curr_user
from app.core.auth.models import User
from app.exceptions import TenderNotFound, UserNotResponsible, VersionNotFound

from app.usecase.tenders import usecase

from app.logger import logger

router = APIRouter()


@router.put("/{tender_id}/rollback/{version}")
async def rollback_to_version(
        tender_id: str,
        version: int,
        user: User = Depends(get_curr_user)
):
    if not isinstance(tender_id, str) or not tender_id:
        raise HTTPException(status_code=422, detail="tender_id must be a non-empty string")

    if not isinstance(version, int) or not version:
        raise HTTPException(status_code=422, detail="version must be an integer and greater than 0")

    async with async_session_maker() as session:

        try:
            tender = await usecase.rollback_to_version(session, tender_id, user, version)
        except TenderNotFound:
            logger.warning("Tender %s not found", tender_id)
            raise HTTPException(status_code=404, detail="Tender %s not found" % tender_id)
        except UserNotResponsible:
            logger.warning("User %s not responsible", user)
            raise HTTPException(status_code=403, detail="You are not responsible to this tender")
        except VersionNotFound:
            logger.warning("Version %s not found", version)
            raise HTTPException(status_code=404, detail="Version %s not found" % version)

        return {
            "message": "Tender rolled back to the specified version successfully.",
            "tender id": tender.id,
            "new description": tender.description,
            "new version": tender.version
        }