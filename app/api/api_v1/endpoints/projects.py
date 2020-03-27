from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from starlette import status

from app import crud
from app import schemas
from app.api.utils.db import get_db
from app.api.utils.security import get_current_active_user
from app.db.paginator import Paginator
from app.models import Project, ProjectUser
from app.resources import strings
from app.schemas import ProjectRole
from app.schemas.common import PaginatedResponse

router = APIRouter()


@router.get("/",
            response_model=PaginatedResponse[schemas.Project],
            name='projects:list-projects',
            dependencies=[Depends(get_current_active_user)])
def read_projects(paginator: Paginator = Depends(),
                  db: Session = Depends(get_db),
                  client: int = Query(None, gt=0),
                  name: str = Query(None, min_length=3, max_length=250)):
    """
    Retrieve projects..
    """
    filters = []
    if client:
        filters.append(Project.client_id == client)
    if name:
        filters.append(func.lower(Project.name).like(f'%{name}%'))

    projects = crud.project.get_multi_paginated(db, filters=filters, paginator=paginator)
    return projects


@router.get('/user',
            response_model=PaginatedResponse[schemas.ProjectUser],
            name='projects:list-project-users',
            dependencies=[Depends(get_current_active_user)])
def read_project_users(paginator: Paginator = Depends(),
                       db: Session = Depends(get_db),
                       project: int = Query(None, gt=0),
                       user: int = Query(None, gt=0),
                       role: ProjectRole = None):
    """
    Retrieve project - user associations.
    """

    filters = []
    if project:
        filters.append(ProjectUser.project_id == project)
    if user:
        filters.append(ProjectUser.user_id == user)
    if role:
        filters.append(ProjectUser.role == role.value)

    associations = crud.project_user.get_multi_paginated(db, filters=filters, paginator=paginator)
    return associations


@router.post('/user',
             response_model=schemas.ProjectUser,
             name='projects:create-project-user',
             dependencies=[Depends(get_current_active_user)])
def create_project_user(project_user: schemas.ProjectUserCreate,
                        db: Session = Depends(get_db)):
    """
    Create an association object between project and user. In other words assign user to a project.
    User is firstly granted with no permissions and project manager decides whether he can actually join the project.

    - **userId**: Id of a user
    - **projectId**: Id of a project
    - **joinMessage**: Message that will be displayed for a project manager.
    """

    if crud.project_user.exists(db, user_id=project_user.user_id, project_id=project_user.project_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=strings.USER_ALREADY_IN_PROJECT)
    project_user = crud.project_user.create(db, obj_in=project_user)
    return project_user


@router.patch('/user/{association_id}',
              response_model=schemas.ProjectUser,
              name='projects:patch-project-user',
              dependencies=[Depends(get_current_active_user)])
def update_project_user_role(*,
                             db: Session = Depends(get_db),
                             association_id: int,
                             project_user_in: schemas.ProjectUserUpdate):
    """
    Update project - user association data.
    """

    project_user = crud.project_user.get(db, association_id)
    if not project_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=strings.NOT_FOUND_ERROR)
    project_user = crud.project_user.update(db, db_obj=project_user, obj_in=project_user_in)
    return project_user
