from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql+psycopg2://{settings.database_username}:{quote_plus(settings.database_password)}@{settings.database_hostname}/{settings.database_name}'

engine = create_engine(url=SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False,autoflush=False,bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()