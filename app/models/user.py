import datetime

from sqlalchemy import Column, String, Integer, Boolean, DateTime, TypeDecorator

from app.db.base_class import Base


# noinspection PyAbstractClass
class AwareDateTime(TypeDecorator):
    impl = DateTime

    def process_result_value(self, value, dialect):
        return value.replace(tzinfo=datetime.timezone.utc)


class User(Base):
    __tablename__ = 'core_user'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String())
    first_name = Column(String)
    last_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_staff = Column(Boolean)
    is_eeci = Column(Boolean, default=False)
    date_joined = Column(AwareDateTime)
    is_superuser = Column(Boolean, default=False)
    full_name = Column('FullName', String)
    hashed_password = Column('password', String)
