import datetime

from sqlalchemy import literal
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models import Project, ProjectUser
from app.schemas import ProjectUserCreate, ProjectUserUpdate, ProjectRole


class CRUDProjectUser(CRUDBase[Project, ProjectUserCreate, ProjectUserUpdate]):
    def create(self, db_session: Session, *, obj_in: ProjectUserCreate) -> ProjectUser:
        db_obj = ProjectUser(**obj_in.dict(),
                             role=ProjectRole.awaiting.value,
                             is_project_favourite=False,
                             date_requested=datetime.datetime.now(datetime.timezone.utc))
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

    @staticmethod
    def exists(db_session: Session, *, user_id: int, project_id: int):
        result = (db_session.query(literal(True))
                  .filter(ProjectUser.user_id == user_id,
                          ProjectUser.project_id == project_id)
                  .first()
                  )
        return result is not None


project: CRUDBase = CRUDBase[Project, None, None](Project)
project_user = CRUDProjectUser(ProjectUser)
