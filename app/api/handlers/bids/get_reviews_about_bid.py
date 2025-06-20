from fastapi import Depends, HTTPException

from app.database import async_session_maker

from app.core.auth.dependencies import get_curr_user
from app.core.auth.models import User
from app.exceptions import DontHavePermissions, TenderNotFound, ReviewsNotFound, OrganizationNotFound

from app.logger import logger
from fastapi import APIRouter
from app.usecase.bids import usecase

router = APIRouter()


@router.get("/{tender_id}/reviews")
async def get_reviews(
        tender_id: str,
        author_username: str,
        user: User = Depends(get_curr_user),
):
    async with async_session_maker():

        try:
            reviews = await usecase.get_reviews_for_bid(tender_id, author_username, user)

        except TenderNotFound as e:
            logger.warning("Tender not found %s", e)
            raise HTTPException(detail="Tender not found", status_code=404)

        except OrganizationNotFound:
            logger.warning("Organization not found")
            raise HTTPException(detail="User organization not found", status_code=404)

        except DontHavePermissions as e:
            logger.warning("User dont have permissions to view reviews.")
            raise HTTPException(detail="User dont have permissions to view reviews.", status_code=403)

        except ReviewsNotFound:
            logger.warning("Reviews not found")
            raise HTTPException(detail="Reviews not found", status_code=404)

        return {
            "message": "OK",
            "reviews": reviews
        }