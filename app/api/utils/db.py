from app.db.session import SessionLocal


# Dependency
def get_db():
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if db:
            db.close()

