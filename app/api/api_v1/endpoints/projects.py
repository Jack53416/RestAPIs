from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app import crud
from app import schemas
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
def create_project_user(project_user: schemas.ProjectUserCreate, db: Session = Depends(get_db)):
    if crud.project_user.exists(db, user_id=project_user.user_id, project_id=project_user.project_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User is already in this project')
    project_user = crud.project_user.create(db, obj_in=project_user)
    return project_user
