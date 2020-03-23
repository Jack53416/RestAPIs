from sqlalchemy import Column, String, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Session

from app import schemas
from app.db.base_class import Base


class User(Base):
    __tablename__ = 'core_user'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    full_name = Column('FullName', String)
    hashed_password = Column('password', String)
