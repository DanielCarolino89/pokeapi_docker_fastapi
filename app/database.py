import os
from contextlib import contextmanager
from os import getenv

from sqlalchemy import create_engine, text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, sessionmaker, Session


class Base(MappedAsDataclass, DeclarativeBase):
    pass


DATABASE_NAME: str = getenv("DATABASE_NAME", "easetrack")
_database_url = getenv("DATABASE_URL", "").strip()
DATABASE_URL: str = _database_url or (
    "sqlite:///:memory:" if getenv("APP_ENV") == "test" else "db"
)
DB_LOCK_TIMEOUT_MS = int(getenv("DB_LOCK_TIMEOUT_MS", "5000"))

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=1800,  # 30min
    # pool_size=5,
    # max_overflow=10,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def create_database(db_name: str | None = DATABASE_NAME) -> None:
    """Create a new database with the given name.

    Args:
        db_name (str | None): Input parameter required by this operation.

    Returns:
        None: This function does not return a value.
    """
    admin_engine = create_engine(DATABASE_URL.replace(DATABASE_NAME, "postgres"))
    with admin_engine.connect() as conn:
        conn.execution_options(isolation_level="AUTOCOMMIT")
        try:
            conn.execute(text(f'CREATE DATABASE "{db_name}"'))
            print(f"Database {db_name} created successfully.")
        except ProgrammingError:
            print(f"Database {db_name} already exists.")


@contextmanager
def get_sync_session():
    """Provide a transactional scope around a series of operations.

    Returns:
        Any: Resolved resource returned by this retrieval operation.
    """
    session = SessionLocal()
    _apply_lock_timeout(session)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def _apply_lock_timeout(session: Session) -> None:
    """Apply a bounded lock wait for PostgreSQL sessions.

    This avoids hanging requests when a row/table lock cannot be acquired promptly.
    """
    bind = session.get_bind()
    if not bind or bind.dialect.name != "postgresql":
        return

    timeout_ms = max(DB_LOCK_TIMEOUT_MS, 1)
    session.execute(text(f"SET lock_timeout = '{timeout_ms}ms'"))


def get_session():
    """Provide a transactional scope around a series of operations.

    Returns:
        Any: Resolved resource returned by this retrieval operation.
    """
    with Session(engine) as session:
        _apply_lock_timeout(session)
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
