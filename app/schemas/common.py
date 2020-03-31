import datetime
import re

from typing import Generic, TypeVar, List, Match
from pydantic import BaseModel, HttpUrl, AnyUrl
from pydantic.generics import GenericModel

DataT = TypeVar('DataT')


def to_camel_case(snake_str: str) -> str:
    first, *others = snake_str.split('_')
    return ''.join([first.lower(), *map(str.title, others)])


def to_snake_case(camel_str: str) -> str:
    reg = r'(.+?)([A-Z])'

    def snake(match: Match):
        return f'{match.group(1).lower()}_{match.group(2).lower()}'

    return re.sub(reg, snake, camel_str, 0)


def convert_datetime_to_realword(dt: datetime.datetime) -> str:
    return dt.replace(tzinfo=datetime.timezone.utc).isoformat().replace("+00:00", "Z")


class RWModel(BaseModel):
    class Config(object):
        allow_population_by_field_name = True
        json_encoders = {datetime.datetime: convert_datetime_to_realword}
        alias_generator = to_camel_case
        orm_mode = True


class Links(BaseModel):
    next: AnyUrl = None
    previous: AnyUrl = None
    current: AnyUrl
    last: AnyUrl


class PaginatedResponse(RWModel, GenericModel, Generic[DataT]):
    """
    Paginated response of given content
    """
    count: int = 0
    pages: int = 0
    page_size: int
    links: Links = None
    data: List[DataT]
