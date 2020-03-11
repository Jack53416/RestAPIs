from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class ProjectRole(str, Enum):
    manager = 'project_manager',
    integrator = 'integrator'
    awaiting = 'awaiting'


class ClientBase(BaseModel):
    name: str


class Client(ClientBase):
    id: int

    class Config:
        orm_mode = True


class ProjectBase(BaseModel):
    name: str
    client_id: int = Field(..., gt=0)
    integrity_path: str
    is_active: bool = True
    contacts: str
    description: str
    react_on_new_cp: bool = False
    last_ptc_update: datetime = None
    integration_name: str = None


class Project(ProjectBase):
    id: int

    class Config:
        orm_mode = True


class ProjectUserBase(BaseModel):
    user_id: int = Field(..., gt=0, description='Id of an existing user')
    project_id: int = Field(..., gt=0, description='Id of an existing project')
    join_message: str = Field(..., max_length=300,
                              description='Join request message, that will be displayed to '
                                          'a project manager')


class ProjectUserCreate(ProjectUserBase):
    pass


class ProjectUser(ProjectUserBase):
    id: int
    role: ProjectRole = ProjectRole.awaiting
    is_project_favourite: bool = False
    date_joined: datetime = None
    date_requested: datetime = None

    class Config:
        orm_mode = True
