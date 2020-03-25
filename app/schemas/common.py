import datetime

from typing import Generic, TypeVar, List
from pydantic import BaseModel
from pydantic.generics import GenericModel

DataT = TypeVar('DataT')


def to_camel_case(snake_str: str) -> str:
    first, *others = snake_str.split('_')
    return ''.join([first.lower(), *map(str.title, others)])


def convert_datetime_to_realword(dt: datetime.datetime) -> str:
    return dt.replace(tzinfo=datetime.timezone.utc).isoformat().replace("+00:00", "Z")


class RWModel(BaseModel):
    class Config(object):
        allow_population_by_field_name = True
        json_encoders = {datetime.datetime: convert_datetime_to_realword}
        alias_generator = to_camel_case
        orm_mode = True


class Links(BaseModel):
    next: str = None
    previous: str = None
    current: str = None
    last: str


class PaginatedResponse(RWModel, GenericModel, Generic[DataT]):
    """
    Paginated response of given content
    """
    count: int = None
    pages: int = None
    page_size: int = None
    links: Links = None
    data: List[DataT] = []
