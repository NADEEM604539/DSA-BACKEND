"""
db.py
SQLAlchemy MySQL connection + session management
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from config import settings

# -----------------------------
# 1) Base declarative class
# -----------------------------
Base = declarative_base()

# -----------------------------
# 2) SQLAlchemy Engine (TiDB SSL Enabled)
# -----------------------------
engine = create_engine(
    settings.database_url,
    echo=False,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    pool_timeout=30,
    future=True,
    connect_args={
        "ssl": {
            "ca": settings.DB_SSL_CA
        }
    }
)

# -----------------------------
# 3) Session factory
# -----------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False
)

scoped_session_factory = scoped_session(SessionLocal)

# -----------------------------
# 4) Dependency for FastAPI
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

# -----------------------------
# 5) Init DB
# -----------------------------
def init_db():
    from models import Base as ModelsBase
    print("Creating tables if not exist...")
    ModelsBase.metadata.create_all(bind=engine)
    print("[INFO] All tables are ready.")