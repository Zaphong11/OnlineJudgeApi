from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.config import settings

"""Database connection and session management for the Online Judge application."""

engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

from models import language, result, submission

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()