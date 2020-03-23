from app import schemas

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud
from app.api.utils.db import get_db

router = APIRouter()


@router.get("/", response_model=List[schemas.Project])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    projects = crud.project.get_multi(db, skip=skip, limit=limit)
    return projects


@router.get('/user', response_model=List[schemas.ProjectUser])
def read_project_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    associations = crud.project_user.get_multi(db, skip=skip, limit=limit)
    return associations


@router.post('/user', response_model=schemas.ProjectUser)
def create_project_user(association: schemas.ProjectUserCreate, db: Session = Depends(get_db)):
    project_user = crud.project_user.create(db, obj_in=association)
    return project_user
