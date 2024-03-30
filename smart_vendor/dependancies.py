from smart_vendor.database import SessionLocal


def get_db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()