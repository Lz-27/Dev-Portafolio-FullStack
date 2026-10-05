"""
models/project.py
─────────────────
Modelo SQLAlchemy para la tabla `projects`.
Refleja los proyectos del portafolio con soporte de filtrado por categoría.
"""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(500), nullable=False)
    detalles: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Categorización
    categoria: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    categoria_label: Mapped[str] = mapped_column(String(100), nullable=False)

    # Tecnologías almacenadas como string JSON (["React", "Python", ...])
    tecnologias: Mapped[str] = mapped_column(Text, default="[]", nullable=False)

    # URLs
    github: Mapped[str | None] = mapped_column(String(500), nullable=True)
    demo: Mapped[str | None] = mapped_column(String(500), nullable=True)
    imagen: Mapped[str | None] = mapped_column(String(500), nullable=True)

    destacado: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Project id={self.id} slug={self.slug!r} categoria={self.categoria!r}>"
