from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from app import crud
from app import schemas
from app.api.utils.db import get_db
from app.api.utils.security import get_current_active_user
from app.models.user import User as DBUser

router = APIRouter()


@router.get("/", response_model=List[schemas.Project])
def read_projects(skip: int = 0,
                  limit: int = 100,
                  db: Session = Depends(get_db),
                  current_user: DBUser = Depends(get_current_active_user)):
    projects = crud.project.get_multi(db, skip=skip, limit=limit)
    return projects


@router.get('/user', response_model=List[schemas.ProjectUser])
def read_project_users(skip: int = 0,
                       limit: int = 100,
                       db: Session = Depends(get_db),
                       current_user: DBUser = Depends(get_current_active_user)):
    associations = crud.project_user.get_multi(db, skip=skip, limit=limit)
    return associations


@router.post('/user', response_model=schemas.ProjectUser)
def create_project_user(project_user: schemas.ProjectUserCreate,
                        db: Session = Depends(get_db),
                        current_user: DBUser = Depends(get_current_active_user)):
    if crud.project_user.exists(db, user_id=project_user.user_id, project_id=project_user.project_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User is already in this project')
    project_user = crud.project_user.create(db, obj_in=project_user)
    return project_user


@router.patch('/user/{association_id}', response_model=schemas.ProjectUser)
def update_project_user_role(*,
                             db: Session = Depends(get_db),
                             association_id: int,
                             project_user_in: schemas.ProjectUserUpdate,
                             current_user: DBUser = Depends(get_current_active_user)):

    project_user = crud.project_user.get(db, association_id)
    if not project_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Searched object does not exist in database')
    project_user = crud.project_user.update(db, db_obj=project_user, obj_in=project_user_in)
    return project_user

