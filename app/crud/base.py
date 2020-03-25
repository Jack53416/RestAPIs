from typing import List, Optional, Generic, TypeVar, Type, Iterable

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.paginator import Paginator
from app.db.base_class import Base
from app.schemas.common import PaginatedResponse

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def get(self, db_session: Session, id: int) -> Optional[ModelType]:
        return db_session.query(self.model).filter(self.model.id == id).first()

    def get_multi_paginated(self,
                            db_session: Session, *,
                            filters: Iterable[any] = None,
                            paginator: Paginator) -> PaginatedResponse:
        query = db_session.query(self.model)
        if filters:
            query = query.filter(*filters)
        return paginator.paginate(db_session, model=self.model, base_query=query)

    def get_multi(self, db_session: Session, *, skip=0, limit=100, filters: Iterable[any] = None) -> List[ModelType]:
        # ToDo(Jacek): MSSQL requires order by with offset and limit on a query level
        if filters:
            return db_session.query(self.model).filter(*filters).offset(skip).limit(limit).all()
        return db_session.query(self.model).offset(skip).limit(limit).all()

    def create(self, db_session: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = obj_in.dict()
        db_obj = self.model(**obj_in_data)
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

    def update(
            self, db_session: Session, *, db_obj: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(skip_defaults=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

    def remove(self, db_session: Session, *, id: int) -> ModelType:
        obj = db_session.query(self.model).get(id)
        db_session.delete(obj)
        db_session.commit()
        return obj
