from sqlalchemy import inspect
from sqlalchemy.ext.declarative import declarative_base, declared_attr


def create_col_lookup(mapper):
    return {c.name: k for k, c in mapper.columns.items()}


class ColBase(object):

    @classmethod
    def create_col_lookup(cls):
        return {c.name: k for k, c in inspect(cls).mapper.columns.items()}

    @classmethod
    def map_db_columns(cls, **kwargs):
        mapping = cls.create_col_lookup()
        return {mapping[k]: v for k, v in kwargs.items() if k in mapping}


Base = declarative_base(cls=ColBase)
