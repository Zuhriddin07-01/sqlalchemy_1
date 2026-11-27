import os
from sqlalchemy import create_engine, event
from sqlalchemy.engine import make_url
from sqlalchemy.orm import DeclarativeBase, sessionmaker


def make_engine(database_url):
    url = make_url(database_url)
    is_sqlite = url.get_backend_name() == "sqlite"
    options = {"check_same_thread": False} if is_sqlite else {}
    database_engine = create_engine(url, connect_args=options)
    if is_sqlite:
        @event.listens_for(database_engine, "connect")
        def enable_foreign_keys(connection, _):
            cursor = connection.cursor()
            try:
                cursor.execute("PRAGMA foreign_keys=ON")
            finally:
                cursor.close()
    return database_engine


engine = make_engine(os.getenv("DATABASE_URL", "sqlite:///./shop.db"))

SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    with SessionLocal() as session:
        yield session
