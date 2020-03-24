from datetime import datetime

from pydantic import BaseModel

from app.schemas import RWModel


class UserBase(BaseModel):
    email: str = None
    username: str = None
    first_name: str = None
    last_name: str = None
    full_name: str = None
    is_active: bool = False
    is_superuser: bool = False
    is_staff: bool = False
    is_eeci: bool = False


class UserBaseInDb(RWModel, UserBase):
    id: int = None


# Properties to receive via API on creation
class UserCreate(UserBaseInDb):
    email: str
    username: str
    password: str
    first_name: str
    last_name: str
    is_staff: bool = True
    is_eeci: bool = False


# Properties to receive via API on update
class UserUpdate(UserBaseInDb):
    password: str = None


# Additional properties to return via API
class User(UserBaseInDb):
    date_joined: datetime = None


# Additional properties stored in DB
class UserInDb(UserBaseInDb):
    hashed_password: str
