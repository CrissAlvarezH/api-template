from typing import Generator

from app.db.session import create_session


def get_db() -> Generator:
    try:
        db = create_session()
        yield db
    finally:
        db.close()
