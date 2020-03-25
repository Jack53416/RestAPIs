from math import ceil
from typing import Optional

from fastapi import Query
from sqlalchemy.orm import Session
from sqlalchemy.orm import Query as DBQuery
from starlette.requests import Request

from app.db.base_class import Base
from app.schemas.common import Links, PaginatedResponse


class Paginator(object):
    # ToDo(Jacek): Specify default ordering for each model and use it in paginator

    default_page_size = 100
    default_page = 1
    max_page_size = 300

    def __init__(self,
                 request: Request,
                 ordering: str = None,
                 page: int = Query(default_page, ge=1),
                 page_size: int = Query(default_page_size, ge=1, le=max_page_size)):
        self.request = request
        self.page = page
        self.page_size = page_size
        self.ordering = ordering
        self.total_pages = 0

    def parse_order(self, model: Base, query_fields: any) -> any:
        if self.ordering is None:
            return query_fields['Id']

        desc = self.ordering[0] == '-'
        ordering = self.ordering[1:] if desc else self.ordering

        order_field = getattr(model, ordering, None)
        order_key = order_field.expression.name if order_field else 'Id'

        order_field = query_fields[order_key].desc() if desc else query_fields[order_key]
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

    def get_total_pages(self, total_records: int) -> int:
        self.total_pages = ceil(total_records / self.page_size)
        return self.total_pages

    def generate_links(self) -> Links:
        return Links.construct(
            next=self.next_url,
            previous=self.previous_url,
            current=self.current_url,
            last=self.last_url
        )

    def paginate(self, db_session: Session, model: Base, base_query: DBQuery) -> PaginatedResponse:

        data_cte = base_query.cte(name='data_cte')
        count_cte = data_cte.count().cte(name='count_cte')
        q = (db_session.query(data_cte, count_cte)
             .order_by(self.parse_order(model, data_cte.c))
             .offset((self.page - 1) * self.page_size)
             .limit(self.page_size)
             )
        result = q.all()

        total_records = result[0].tbl_row_count if result else 0
        data = [model.map_db_columns(**r._asdict()) for r in result]

        return PaginatedResponse.construct(
            count=len(data),
            pages=self.get_total_pages(total_records),
            page_size=self.page_size,
            links=self.generate_links(),
            data=data
        )
