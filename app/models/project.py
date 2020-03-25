from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime

from app.db.base_class import Base


class Clients(Base):
    __tablename__ = 't_clients'

    id = Column('Id', Integer, primary_key=True, index=True)
    name = Column('Name', String)


class Project(Base):
    __tablename__ = 't_projects'

    id = Column('Id', Integer, primary_key=True, index=True)
    name = Column('Name', String)
    client_id = Column('ClientId', Integer, ForeignKey('t_clients.Id'))
    integrity_path = Column('IntegrityPath', String)
    is_active = Column('Active', Boolean)
    contacts = Column('Contacts', String)
    description = Column('Description', String)
    # Slug
    # ParentId
    react_on_new_cp = Column('ReactOnNewCP', Boolean)
    last_ptc_update = Column('LastUpdatePTC', DateTime)
    # RegexId
    integration_name = Column('IntegrationName', String)


class ProjectUser(Base):
    __tablename__ = 't_project_user'

    id = Column('Id', Integer, primary_key=True, index=True)
    user_id = Column('UserId', ForeignKey('core_user.id'))
    project_id = Column('ProjectId', ForeignKey('t_projects.Id', use_alter=True), nullable=False)
    role = Column('Role', String)
    is_project_favourite = Column('IsFavouriteProject', Boolean)
    date_joined = Column('JoinDate', DateTime)
    date_requested = Column('RequestDate', DateTime)
    join_message = Column('JoinMessage', String)
