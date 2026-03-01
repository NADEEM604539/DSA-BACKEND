# db.py
"""
SQLAlchemy engine setup for TiDB Cloud with SSL support
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings

# Create the SQLAlchemy engine using our Settings
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,  # optional, recommended for cloud DBs
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()