# db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import settings
import os

# Ensure the CA file path exists in Vercel
ssl_ca_path = os.path.join(os.path.dirname(__file__), settings.DB_SSL_CA)

# SQLAlchemy engine with SSL
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    connect_args={
        "ssl": {"ca": ssl_ca_path}  # required for TiDB Cloud
    }
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()