import os
from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, drop_database

from app.core.config import Settings
from app.db.base_class import Base


@pytest.fixture(scope="session")
def db():
    # create database for test purpose
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    db_name = f'test_{os.getenv("DB_NAME")}_{timestamp}'
    os.environ["POSTGRES_DB"] = db_name

    settings = Settings()
    engine = create_engine(settings.PG_DNS)
    create_database(engine.url)

    # create tables
    Base.metadata.create_all(engine)

    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()

    yield session

    session.close()

    if os.getenv("TEST_KEEP_PG_DB") != "true":
        drop_database(engine.url)
