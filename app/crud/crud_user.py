from datetime import datetime, timezone
from typing import Optional, List

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.paginator import Paginator
from app.models.user import User
from app.schemas.common import PaginatedResponse
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import verify_password, get_password_hash
from app.crud.base import CRUDBase


# noinspection PyMethodMayBeStatic
class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def search(self, db_session: Session, *, expr: str, paginator: Paginator) -> PaginatedResponse:

        search = f'%{expr}%'
        query = db_session.query(self.model).filter(
            func.lower(User.full_name).like(search) |
            func.lower(User.username).like(search)
        )
        return paginator.paginate(db_session, self.model, query)

    def get_by_email(self, db_session: Session, *, email: str) -> Optional[User]:
        return db_session.query(User).filter(User.email == email).first()

    def create(self, db_session: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            **obj_in.dict(exclude={'password'}),
            hashed_password=get_password_hash(obj_in.password),
            date_joined=datetime.now(timezone.utc)
        )
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

    def authenticate(
        self, db_session: Session, *, email: str, password: str
    ) -> Optional[User]:
        user = self.get_by_email(db_session, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user = CRUDUser(User)
