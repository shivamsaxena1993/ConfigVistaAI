"""
====================================================================
File: database.py

Project : ConfigVista AI
Author  : Shivam Saxena
Purpose :
    Central database configuration and connection manager.

Responsibilities
----------------
1. Create SQLAlchemy Engine
2. Create Session Factory
3. Create Declarative Base
4. Enable SQLite Foreign Keys
5. Provide reusable DB sessions
6. Test database connectivity

====================================================================
"""

from pathlib import Path
from contextlib import contextmanager
import logging
import yaml

from sqlalchemy import create_engine
from sqlalchemy import event
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


# -------------------------------------------------------------------
# Logging
# -------------------------------------------------------------------

logger = logging.getLogger(__name__)


# -------------------------------------------------------------------
# Project Paths
# -------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CONFIG_FILE = PROJECT_ROOT / "configs" / "database_config.yaml"


# -------------------------------------------------------------------
# Read Database Configuration
# -------------------------------------------------------------------

def load_database_config():
    """
    Reads database configuration from YAML file.
    """

    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            f"Database configuration not found : {CONFIG_FILE}"
        )

    with open(CONFIG_FILE, "r", encoding="utf-8") as file:
        return yaml.safe_load(file)


config = load_database_config()

DATABASE_PATH = PROJECT_ROOT / config["database"]["path"]

DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


# -------------------------------------------------------------------
# SQLAlchemy Engine
# -------------------------------------------------------------------

engine = create_engine(

    DATABASE_URL,

    echo=False,

    future=True

)


# -------------------------------------------------------------------
# Enable SQLite Foreign Keys
# -------------------------------------------------------------------

@event.listens_for(engine, "connect")
def enable_sqlite_foreign_keys(dbapi_connection, connection_record):

    cursor = dbapi_connection.cursor()

    cursor.execute("PRAGMA foreign_keys=ON")

    cursor.close()


# -------------------------------------------------------------------
# Session Factory
# -------------------------------------------------------------------

SessionLocal = sessionmaker(

    bind=engine,

    autoflush=False,

    autocommit=False,

    future=True

)


# -------------------------------------------------------------------
# Base Class
# -------------------------------------------------------------------

Base = declarative_base()


# -------------------------------------------------------------------
# Session Context Manager
# -------------------------------------------------------------------

@contextmanager
def get_session():
    """
    Provides transactional database session.

    Example:

        with get_session() as session:
            ...

    """

    session = SessionLocal()

    try:

        yield session

        session.commit()

    except Exception:

        session.rollback()

        raise

    finally:

        session.close()


# -------------------------------------------------------------------
# Database Connectivity Test
# -------------------------------------------------------------------

def test_connection():

    """
    Tests database connectivity.
    """

    try:

        with engine.connect():

            logger.info("Database connection successful.")

            return True

    except Exception as ex:

        logger.error(f"Database connection failed : {ex}")

        return False


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------

if __name__ == "__main__":

    print("=" * 60)

    print("ConfigVista AI - Database Connection Test")

    print("=" * 60)

    print(f"Database URL : {DATABASE_URL}")

    status = test_connection()

    if status:

        print("\nDatabase connection successful.")

    else:

        print("\nDatabase connection failed.")