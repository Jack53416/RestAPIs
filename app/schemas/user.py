from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool = Field(True, alias='isActive')

    class Config:
        orm_mode = True
