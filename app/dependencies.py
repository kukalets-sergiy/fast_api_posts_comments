from app.database import async_session_maker


def get_db():
    db = async_session_maker()
    try:
        yield db
    finally:
        db.close()


