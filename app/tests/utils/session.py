from sqlalchemy import orm

from app.db.session import SessionLocal

TestSession = orm.scoped_session(SessionLocal)
