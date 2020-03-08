from datetime import datetime

from sqlalchemy.orm import Session

from . import models
from app import schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_projects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Project).offset(skip).limit(limit).all()


def get_project_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.ProjectUser).offset(skip).limit(limit).all()


def create_project_user(db: Session, association: schemas.ProjectUserCreate):
    db_project_user = models.ProjectUser(**association.dict(),
                                         role=schemas.ProjectRole.awaiting.value,
                                         date_requested=datetime.now(),
                                         is_project_favourite=False,
                                         date_joined=datetime.now())
    db.add(db_project_user)
    db.commit()
    db.refresh(db_project_user)

    return db_project_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
