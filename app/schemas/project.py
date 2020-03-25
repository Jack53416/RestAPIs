import datetime
from enum import Enum

from pydantic import BaseModel, Field

from app.schemas.common import RWModel


class ProjectRole(str, Enum):
    manager = 'project_manager',
    integrator = 'integrator'
    awaiting = 'awaiting'


class Client(BaseModel):
    name: str
    id: int


class ProjectBase(BaseModel):
    name: str = None
    client_id: int = None
    integrity_path: str = None
    is_active: bool = None
    contacts: str = None
    description: str = None
    react_on_new_cp: bool = None
    last_ptc_update: datetime.datetime = None
    integration_name: str = None


class ProjectBaseInDb(RWModel, ProjectBase):
    id: int


class Project(ProjectBaseInDb):
    pass


class ProjectUserBase(BaseModel):
    user_id: int = None
    project_id: int = None
    join_message: str = None


class ProjectUserBaseInDb(RWModel, ProjectUserBase):
    id: int = None


class ProjectUserCreate(ProjectUserBaseInDb):
    user_id: int = Field(..., gt=0, description='Id of a user that will join a project')
    project_id: int = Field(..., gt=0)
    join_message: str = Field(..., description='Message that will be displayed to a project manager')


class ProjectUserUpdate(ProjectUserBaseInDb):
    role: ProjectRole


class ProjectUser(ProjectUserBaseInDb):
    role: ProjectRole = ProjectRole.awaiting
    is_project_favourite: bool
    date_joined: datetime.datetime = None
    date_requested: datetime.datetime
