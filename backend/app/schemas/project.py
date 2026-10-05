"""
schemas/project.py
──────────────────
Schemas Pydantic para el recurso Project.
Patrón: Create → Update → InDB → Response
"""
from __future__ import annotations

import json
from datetime import datetime

from pydantic import BaseModel, Field, field_validator


# ── Base ──────────────────────────────────────────────────────────────────────
class ProjectBase(BaseModel):
    """Campos comunes compartidos entre Create y Update."""

    titulo: str = Field(..., min_length=3, max_length=200)
    descripcion: str = Field(..., min_length=10, max_length=500)
    detalles: str | None = Field(default=None)
    categoria: str = Field(..., max_length=50)
    categoria_label: str = Field(..., max_length=100)
    tecnologias: list[str] = Field(default_factory=list)
    github: str | None = Field(default=None, max_length=500)
    demo: str | None = Field(default=None, max_length=500)
    imagen: str | None = Field(default=None, max_length=500)
    destacado: bool = Field(default=False)


# ── Create ────────────────────────────────────────────────────────────────────
class ProjectCreate(ProjectBase):
    """Schema para crear un proyecto (POST /projects/)."""

    slug: str = Field(..., min_length=3, max_length=100, pattern=r"^[a-z0-9-]+$")


# ── Update ────────────────────────────────────────────────────────────────────
class ProjectUpdate(BaseModel):
    """Schema para actualizar parcialmente un proyecto (PUT /projects/{id})."""

    titulo: str | None = Field(default=None, min_length=3, max_length=200)
    descripcion: str | None = Field(default=None, min_length=10, max_length=500)
    detalles: str | None = None
    categoria: str | None = Field(default=None, max_length=50)
    categoria_label: str | None = Field(default=None, max_length=100)
    tecnologias: list[str] | None = None
    github: str | None = None
    demo: str | None = None
    imagen: str | None = None
    destacado: bool | None = None


# ── Response ──────────────────────────────────────────────────────────────────
class ProjectResponse(BaseModel):
    """Schema de respuesta completo para un proyecto."""

    id: int
    slug: str
    titulo: str
    descripcion: str
    detalles: str | None
    categoria: str
    categoria_label: str
    tecnologias: list[str]
    github: str | None
    demo: str | None
    imagen: str | None
    destacado: bool
    created_at: datetime
    updated_at: datetime

    @field_validator("tecnologias", mode="before")
    @classmethod
    def parse_tecnologias(cls, v: str | list) -> list[str]:
        """Convierte el string JSON almacenado en BD a lista de Python."""
        if isinstance(v, str):
            return json.loads(v)
        return v

    model_config = {"from_attributes": True}


class ProjectListResponse(BaseModel):
    """Respuesta paginada de proyectos."""

    items: list[ProjectResponse]
    total: int
    skip: int
    limit: int
