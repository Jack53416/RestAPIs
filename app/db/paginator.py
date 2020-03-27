from math import ceil
from typing import Optional

from fastapi import Query, HTTPException
from sqlalchemy import inspect, func, select
from sqlalchemy.orm import Session
from sqlalchemy.orm import Query as DBQuery
from sqlalchemy.sql import Selectable, Select
from starlette import status
from starlette.requests import Request

from app.db.base_class import Base
from app.resources import strings
from app.schemas.common import Links, PaginatedResponse


class Paginator(object):
    """
    Custom page paginator class. It utilizes CTE SQL queries to get record count efficiently in a single
    database query
    """

    # ToDo(Jacek): Specify default ordering for each model and use it in paginator
    # ToDo(Jacek): Add suport for multiple field ordering

    default_page_size = 100
    default_page = 1
    max_page_size = 300

    def __init__(self,
                 request: Request,
                 ordering: str = Query(None,
                                       regex='^-?\\w+$',
                                       min_length=2,
                                       description=strings.PAGINATION_ORDERING_DESC,
                                       example='-id'),
                 page: int = Query(default_page,
                                   ge=1,
                                   description=strings.PAGINATION_PAGE_DESC),
                 page_size: int = Query(default_page_size,
                                        ge=1,
                                        le=max_page_size,
                                        alias='page-size',
                                        description=strings.PAGINATION_PAGE_SIZE_DESC)):
        self.request = request
        self.page = page
        self.page_size = page_size
        self.ordering = ordering
        self.total_pages = 0
        self.total_records = 0

    def order_by_primary_key(self, query: Select) -> any:
        try:
            primary_key_name = query.primary_key[0].name
            order_field = query.columns.get(primary_key_name)
        except IndexError:
            return self.order_by_any_field(query)
        return order_field

    @staticmethod
    def order_by_any_field(query: Select) -> any:
        return next(iter(query.columns.values()))

    def parse_order(self, model: Base, query: Select) -> any:

        if self.ordering is None:
            return self.order_by_primary_key(query)

        desc = self.ordering[0] == '-'
        ordering = self.ordering[1:] if desc else self.ordering
        order_field = getattr(model, ordering, None)

        try:
            order_key = order_field.expression.name
            order_field = query.columns[order_key].desc() if desc else query.columns[order_key]
        except (AttributeError, IndexError):
            return self.order_by_primary_key(query)

        return order_field

    @property
    def previous_url(self) -> Optional[str]:
        if self.page == self.default_page:
            return None
        return str(
            self.request.url.include_query_params(
                page=self.page - 1,
            )
        )

    @property
    def next_url(self) -> Optional[str]:
        if self.page >= self.total_pages:
            return None
        return str(
            self.request.url.include_query_params(
                page=self.page + 1,
            )
        )

    @property
    def current_url(self) -> Optional[str]:
        return str(self.request.url)

    @property
    def last_url(self) -> str:
        return str(self.request.url)

    def get_total_pages(self) -> int:
        total_pages = ceil(self.total_records / self.page_size)
        return total_pages

    def generate_links(self) -> Links:
        return Links.construct(
            next=self.next_url,
            previous=self.previous_url,
            current=self.current_url,
            last=self.last_url
        )

    def paginate(self, db_session: Session, model: Base, base_query: DBQuery) -> PaginatedResponse:

        data_cte: Select = base_query.cte(name='data_cte')
        count_cte: Select = select([func.count().label('total')]).select_from(data_cte).cte(name='count_cte')
        q = (db_session.query(data_cte, count_cte)
             .order_by(self.parse_order(model, data_cte))
             .offset((self.page - 1) * self.page_size)
             .limit(self.page_size)
             )
        result = q.all()

        self.total_records = result[0].total if result else 0
        self.total_pages = self.get_total_pages()
        if self.page > self.total_pages:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=strings.NOT_FOUND_ERROR)

        data = [model.map_db_columns(**r._asdict()) for r in result]

        return PaginatedResponse.construct(
            count=self.total_records,
            pages=self.total_pages,
            page_size=self.page_size,
            links=self.generate_links(),
            data=data
        )
