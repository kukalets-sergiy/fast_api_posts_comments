from app.database import SessionLocal


def get_db():
    db = db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


