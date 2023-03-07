import os
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from pydantic.networks import PostgresDsn
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, drop_database

from app.core.config import settings
from app.db.base_class import Base
from app.main import app


@pytest.fixture(scope="session")
def db():
    # create database for test purpose
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    db_name = f'test_{os.getenv("DB_NAME")}_{timestamp}'

    # overwrite postgres database name on config
    settings.POSTGRES_DB = db_name
    settings.PG_DNS = PostgresDsn.build(
        scheme="postgresql",
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_SERVER,
        path=f"/{settings.POSTGRES_DB or ''}",
    )

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


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c
