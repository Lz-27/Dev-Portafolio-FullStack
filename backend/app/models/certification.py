"""
models/certification.py
───────────────────────
Modelo SQLAlchemy para la tabla `certifications`.
Refleja las certificaciones profesionales del portafolio.
"""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base


class Certification(Base):
    __tablename__ = "certifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    titulo: Mapped[str] = mapped_column(String(200), nullable=False)
    emisor: Mapped[str] = mapped_column(String(200), nullable=False)
    fecha: Mapped[str] = mapped_column(String(10), nullable=False)  # "2023"

    categoria: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    categoria_label: Mapped[str] = mapped_column(String(100), nullable=False)

    # Habilidades como string JSON (["Python", "ML", ...])
    habilidades: Mapped[str] = mapped_column(Text, default="[]", nullable=False)

    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    imagen: Mapped[str | None] = mapped_column(String(500), nullable=True)
    credencial: Mapped[str | None] = mapped_column(String(500), nullable=True)

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
        return f"<Certification id={self.id} titulo={self.titulo!r} emisor={self.emisor!r}>"
