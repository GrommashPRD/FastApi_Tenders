from sqlalchemy.exc import SQLAlchemyError

from app.exceptions import OrganizationNotFound, UserNotResponsible, UserAlreadyInOrganization, DatabaseError
from app.core.organizations.dao import OrganizationDAO, OrgResponsibilityDAO


async def add_responsible_users(session, organization_id, user_ids, user):

    organization = await OrganizationDAO.find_by_id(organization_id)
    if not organization:
        raise OrganizationNotFound("Organization not found.", status_code=404)

    org_responsibility = await OrgResponsibilityDAO.find_organization_responsible(
        user_id=user.id
    )
    if not org_responsibility:
        raise UserNotResponsible("You are not responsible for this user.", status_code=403)


    try:
        existing_user_ids = await OrgResponsibilityDAO.add_users_to_organization(
            session=session,
            organization_id=organization_id,
            user_ids=user_ids
        )
    except SQLAlchemyError:
        raise DatabaseError(detail="Failure to create a new record", status_code=500)

    if existing_user_ids:
        raise UserAlreadyInOrganization("User(s) are already responsible", status_code=400)