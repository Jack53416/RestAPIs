from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# eng = create_engine("mssql+pymssql://user:pass@host/db", deprecate_large_types=True)


SQLALCHEMY_DATABASE_URL = 'sqlite:///./test.db'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()