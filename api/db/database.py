# api/db/database.py

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from sqlalchemy import create_engine
from flask import g, current_app
from api.utils.settings import BASE_DIR, DEBUG
from api.utils.config import config

# Initialize db instance
db = SQLAlchemy()  # This is the db object you'll use for ORM

# Database configuration from settings
DB_HOST = config.DB_HOST
DB_PORT = config.DB_PORT
DB_USER = config.DB_USER
DB_PASSWORD = config.DB_PASSWORD
DB_NAME = config.DB_NAME
DB_TYPE = config.DB_TYPE

def get_db_engine(test_mode: bool):
    """
    Creates a SQLAlchemy engine based on the configuration.
    Defaults to PostgreSQL unless overridden to SQLite for testing.
    """
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    if DB_TYPE == "sqlite" or test_mode:
        BASE_PATH = f"sqlite:///{BASE_DIR}"
        DATABASE_URL = BASE_PATH + "/"

        if test_mode:
            DATABASE_URL = BASE_PATH + "test.db"

        return create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

    elif DB_TYPE == "postgresql":
        DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    return create_engine(DATABASE_URL)

# Create the database engine
engine = get_db_engine(DEBUG)

# Session for interacting with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Scoped session for thread safety
db_session = scoped_session(SessionLocal)

# Base class for models
Base = declarative_base()

def create_database():
    """Creates all tables in the database."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """
    Provides a database session. Used in Flask request context.
    Ensures proper cleanup of the session after use.
    """
    # Access the database session through the application context using `current_app`
    if 'db' not in g:
        g.db = db_session()
    return g.db

def close_db(e=None):
    """
    Closes the database session. Called automatically at the end of each request.
    """
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_app(app):
    """
    Initializes the database module with the Flask app.
    - Registers the `close_db` function to be called at the end of each request.
    """
    app.teardown_appcontext(close_db)  # Ensure the db is closed after the request is done
