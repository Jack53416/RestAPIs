from app.crud.base import CRUDBase
from app.models import Project, ProjectUser
from app.schemas import ProjectUserCreate, ProjectUserUpdate

project: CRUDBase = CRUDBase[Project, None, None](Project)
project_user: CRUDBase = CRUDBase[ProjectUser, ProjectUserCreate, ProjectUserUpdate](ProjectUser)
