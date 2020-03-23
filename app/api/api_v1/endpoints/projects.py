from app import schemas

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.api.utils.db import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Project])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    projects = crud.get_projects(db, skip, limit)
    return projects


@router.get('/user', response_model=List[schemas.ProjectUser])
def read_project_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    associations = crud.get_project_users(db, skip, limit)
    return associations


@router.post('/user', response_model=schemas.ProjectUser)
def create_project_user(association: schemas.ProjectUserCreate, db: Session = Depends(get_db)):
    project_user = crud.create_project_user(db, association)
    return project_user
