import os
from dotenv import load_dotenv
from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.logger import logger

# Load environment variables from a .env file
load_dotenv()
# Create a SQLAlchemy database engine
engine = create_engine(os.environ.get("DATABASE_URL"))

# Create a session factory for creating database sessions
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()


def sess_db():
    """
    Dependency to provide a database session.

    Returns:
        session: A SQLAlchemy database session.
    """
    db = SessionFactory()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database Unavailable"
        )
    finally:
        db.close()
