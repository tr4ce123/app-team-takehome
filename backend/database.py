import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)


def db_session():
    session = Session(engine)
    try:
        yield session
    finally:
        session.close()
        

Base = declarative_base()
