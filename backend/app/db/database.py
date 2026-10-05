"""
db/database.py
──────────────
Configuración del engine SQLAlchemy y la sesión.
Soporta SQLite (desarrollo) y PostgreSQL (producción)
simplemente cambiando DATABASE_URL en .env.
"""
from __future__ import annotations

from sqlalchemy import create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings

# ── Engine ────────────────────────────────────────────────────────────────────
_connect_args: dict = {}

if settings.DATABASE_URL.startswith("sqlite"):
    # SQLite requiere check_same_thread=False para funcionar con FastAPI
    _connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=_connect_args,
    # Pool settings razonables para producción
    pool_pre_ping=True,  # Verifica la conexión antes de usarla
    echo=settings.DEBUG,  # Log SQL solo en modo DEBUG
)

# Habilitar WAL mode en SQLite para mejor concurrencia
if settings.DATABASE_URL.startswith("sqlite"):
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):  # noqa: ANN001
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


# ── Session Factory ───────────────────────────────────────────────────────────
SessionLocal: sessionmaker[Session] = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,  # Evita re-queries innecesarias post-commit
)


# ── Base para modelos ORM ─────────────────────────────────────────────────────
class Base(DeclarativeBase):
    """
    Clase base de la que heredan todos los modelos SQLAlchemy.
    DeclarativeBase es la forma moderna (SQLAlchemy 2.x) de definir modelos.
    """
    pass
