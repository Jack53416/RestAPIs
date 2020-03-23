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

    class Config(object):
        orm_mode = True


class ProjectBase(BaseModel):
    name: str
    client_id: int = Field(None, alias='clientId')
    integrity_path: str = Field(None, alias='integrityPath')
    is_active: bool = Field(True, alias='isActive')
    contacts: str = None
    description: str = None
    react_on_new_cp: bool = Field(False, alias='reactOnNewCp')
    last_ptc_update: datetime = Field(None, alias='lastPtcUpdate')
    integration_name: str = Field(None, alias='integrationName')


class Project(ProjectBase):
    id: int

    class Config(object):
        orm_mode = True


class ProjectUserBase(BaseModel):
    user_id: int = Field(..., gt=0, alias='userId')
    project_id: int
    join_message: str = None


class ProjectUserCreate(ProjectUserBase):
    pass


class ProjectUser(ProjectUserBase):
    id: int
    role: ProjectRole = ProjectRole.awaiting
    is_project_favourite: bool
    date_joined: datetime = None
    date_requested: datetime

    class Config(object):
        orm_mode = True
