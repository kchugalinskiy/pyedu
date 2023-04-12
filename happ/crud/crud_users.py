from happ.crud.base import CRUDBase
from happ.models.user import User
from happ.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    pass


user = CRUDUser(User)
