from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app import crud
from app import schemas
from app.api.utils.db import get_db
from app.api.utils.security import get_current_active_superuser, get_current_active_user
from app.models.user import User as DBUser

router = APIRouter()


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate,
                db: Session = Depends(get_db),
                current_user: DBUser = Depends(get_current_active_superuser)):
    db_user = crud.user.get_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.user.create(db, obj_in=user)


@router.get("/", response_model=List[schemas.User])
def read_users(skip: int = 0,
               limit: int = 100,
               db: Session = Depends(get_db),
               current_user: DBUser = Depends(get_current_active_user)):
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int,
              db: Session = Depends(get_db),
              current_user: DBUser = Depends(get_current_active_user)):
    db_user = crud.user.get(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

