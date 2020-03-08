from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    title: str
    description: str = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int = Field(..., alias='ownerId')

    class Config:
        orm_mode = True
