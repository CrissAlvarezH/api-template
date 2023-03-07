from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


def get_db() -> Generator:
    try:
        engine = create_engine(settings.PG_DNS, pool_pre_ping=True)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        db = SessionLocal()
        yield db
    finally:
        db.close()
