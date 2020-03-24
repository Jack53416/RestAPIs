from datetime import datetime

from app import crud
from app.core import config
from app.schemas.user import UserCreate

# make sure all SQL Alchemy models are imported before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
# from app.db import base


def init_db(db_session):
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    # Base.metadata.create_all(bind=engine)

    user = crud.user.get_by_email(db_session, email=config.FIRST_SUPERUSER)
    if not user:
        user_in = UserCreate(
            email=config.FIRST_SUPERUSER,
            username=config.FIRST_SUPERUSER,
            first_name=config.FIRST_SUPERUSER,
            last_name=config.FIRST_SUPERUSER,
            is_staff=True,
            is_active=True,
            is_eeci=True,
            date_joined=datetime.now(),
            password=config.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        crud.user.create(db_session, obj_in=user_in)
