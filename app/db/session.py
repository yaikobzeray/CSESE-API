from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

_is_sqlite = "sqlite" in settings.DATABASE_URL
_is_mysql = "mysql" in settings.DATABASE_URL

# Build engine kwargs depending on the database dialect.
# - SQLite  : needs check_same_thread=False (threading safety flag).
# - MySQL   : needs pool_recycle + pool_pre_ping to survive the server's
#             idle-connection timeout (default 8 h / 28 800 s).  Without
#             these, long-running apps get "MySQL server has gone away".
# - Others  : sensible defaults, no extra connect_args required.
_engine_kwargs: dict = {}

if _is_sqlite:
    _engine_kwargs["connect_args"] = {"check_same_thread": False}
elif _is_mysql:
    _engine_kwargs["pool_recycle"] = 3600          # recycle every 1 h
    _engine_kwargs["pool_pre_ping"] = True          # test conn before use
    _engine_kwargs["pool_size"] = 5
    _engine_kwargs["max_overflow"] = 10

engine = create_engine(settings.DATABASE_URL, **_engine_kwargs)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Yield a database session and guarantee it is closed on exit."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Reusable annotated dependency alias
DbSession = Annotated[Session, Depends(get_db)]

