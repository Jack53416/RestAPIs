from pydantic import BaseModel


class UserBase(BaseModel):
    email: str = None
    is_active: bool = False
    is_superuser: bool = False
    full_name: str = None


class UserBaseInDb(UserBase):
    id: int = None

    class Config(object):
        orm_mode = True


# Properties to receive via API on creation
class UserCreate(UserBaseInDb):
    email: str
    password: str


# Properties to receive via API on update
class UserUpdate(UserBaseInDb):
    password: str = None


# Additional properties to return via API
class User(UserBaseInDb):
    pass


# Additional properties stored in DB
class UserInDb(UserBaseInDb):
    hashed_password: str
