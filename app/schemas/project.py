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
    client_id: int = Field(..., gt=0, alias='clientId')
    integrity_path: str = Field(..., alias='integrityPath')
    is_active: bool = Field(True, alias='isActive')
    contacts: str
    description: str
    react_on_new_cp: bool = Field(False, alias='reactOnNewCp')
    last_ptc_update: datetime = Field(None, alias='lastPtcUpdate')
    integration_name: str = Field(None, alias='integrationName')


class Project(ProjectBase):
    id: int

    class Config:
        orm_mode = True


class ProjectUserBase(BaseModel):
    user_id: int = Field(..., gt=0, description='Id of an existing user', alias='userId')
    project_id: int = Field(..., gt=0, description='Id of an existing project', alias='projectId')
    join_message: str = Field(..., alias='joinMessage', max_length=300,
                              description='Join request message, that will be displayed to '
                                          'a project manager')


class ProjectUserCreate(ProjectUserBase):
    pass


class ProjectUser(ProjectUserBase):
    id: int
    role: ProjectRole = ProjectRole.awaiting
    is_project_favourite: bool = Field(False, alias='isProjectFavourite')
    date_joined: datetime = Field(None, alias='dateJoined')
    date_requested: datetime = Field(None, alias='dateRequested')

    class Config:
        orm_mode = True
