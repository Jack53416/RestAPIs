from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from starlette import status

from app import crud
from app import schemas
from app.api.utils.db import get_db
from app.api.utils.security import get_current_active_superuser, get_current_active_user
from app.db.paginator import Paginator
from app.resources import strings
from app.schemas.common import PaginatedResponse

router = APIRouter()


@router.post("/",
             response_model=schemas.User,
             name='users:create-user',
             dependencies=[Depends(get_current_active_superuser)])
def create_user(user: schemas.UserCreate,
                db: Session = Depends(get_db)):
    """
    Create user. Requires superuser privileges.

    - **email**
    - **username**
    - **password**
    - **firstName**
    - **lastName**
    - **is_staff**
    - **is_eeci**: determine whether user is a verified user
    """

    db_user = crud.user.get_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail=strings.USER_EMAIL_REGISTERED)
    return crud.user.create(db, obj_in=user)


@router.get("/",
            response_model=PaginatedResponse[schemas.User],
            name='users:list-users',
            dependencies=[Depends(get_current_active_user)])
def read_users(paginator: Paginator = Depends(),
               db: Session = Depends(get_db),
               search: str = Query(None, min_length=3, max_length=512)):
    """
    Retrieve users.
    """

    if search:
        return crud.user.search(db, expr=search, paginator=paginator)
    users = crud.user.get_multi_paginated(db, paginator=paginator)
    return users


@router.get("/{user_id}",
            response_model=schemas.User,
            name='users:get-user',
            dependencies=[Depends(get_current_active_user)])
def read_user(user_id: int,
              db: Session = Depends(get_db)):
    """
    Retrieve a specific user by id.
    """

    db_user = crud.user.get(db, id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=strings.USER_DOES_NOT_EXIST)
    return db_user
