import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from starlette.requests import Request


Base = declarative_base()

def create_db_engine():
    engine = create_engine(os.getenv('DATABASE_URL'), echo=True)
    if not database_exists(os.getenv('DATABASE_URL')):
        create_database(os.getenv('DATABASE_URL'))

    Base.metadata.create_all(engine)
    return engine


def create_session_factory(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db(request: Request):
    return request.state.db
