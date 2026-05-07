from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Database URL
DATABASE_URL = "sqlite:///./shop.db"  # SQLite (eng oddiy, fayl yaratadi)

# Engine
engine = create_engine(DATABASE_URL)

# Session
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base
class Base(DeclarativeBase):
    pass