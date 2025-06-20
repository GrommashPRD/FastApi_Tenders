from app.dao.base import BaseDAO
from app.core.auth.models import User


class UsersDAO(BaseDAO):
    model = User
