"""
Database configuration and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL database URL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/swedish_ecommerce"

# Create SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # Check connection health before using
    pool_size=20,        # Maximum number of database connections
    max_overflow=10      # Maximum number of connections beyond pool_size
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

# Dependency to get DB session
def get_db():
    """
    Provide a database session for each request and close it after the request is finished
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()