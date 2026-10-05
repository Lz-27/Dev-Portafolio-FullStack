"""
schemas/certification.py
────────────────────────
Schemas Pydantic para el recurso Certification.
"""
from __future__ import annotations

import json
from datetime import datetime

from pydantic import BaseModel, Field, field_validator


# ── Base ──────────────────────────────────────────────────────────────────────
class CertificationBase(BaseModel):
    titulo: str = Field(..., min_length=3, max_length=200)
    emisor: str = Field(..., min_length=2, max_length=200)
    fecha: str = Field(..., max_length=10, description="Año o fecha (ej: '2023')")
    categoria: str = Field(..., max_length=50)
    categoria_label: str = Field(..., max_length=100)
    habilidades: list[str] = Field(default_factory=list)
    descripcion: str | None = None
    imagen: str | None = Field(default=None, max_length=500)
    credencial: str | None = Field(default=None, max_length=500)


# ── Create ────────────────────────────────────────────────────────────────────
class CertificationCreate(CertificationBase):
    """Schema para crear una certificación (POST /certifications/)."""
    pass


# ── Update ────────────────────────────────────────────────────────────────────
class CertificationUpdate(BaseModel):
    """Schema para actualizar parcialmente una certificación."""

    titulo: str | None = Field(default=None, min_length=3, max_length=200)
    emisor: str | None = Field(default=None, min_length=2, max_length=200)
    fecha: str | None = Field(default=None, max_length=10)
    categoria: str | None = Field(default=None, max_length=50)
    categoria_label: str | None = Field(default=None, max_length=100)
    habilidades: list[str] | None = None
    descripcion: str | None = None
    imagen: str | None = None
    credencial: str | None = None


# ── Response ──────────────────────────────────────────────────────────────────
class CertificationResponse(BaseModel):
    id: int
    titulo: str
    emisor: str
    fecha: str
    categoria: str
    categoria_label: str
    habilidades: list[str]
    descripcion: str | None
    imagen: str | None
    credencial: str | None
    created_at: datetime
    updated_at: datetime

    @field_validator("habilidades", mode="before")
    @classmethod
    def parse_habilidades(cls, v: str | list) -> list[str]:
        """Convierte el string JSON almacenado en BD a lista de Python."""
        if isinstance(v, str):
            return json.loads(v)
        return v

    model_config = {"from_attributes": True}


class CertificationListResponse(BaseModel):
    items: list[CertificationResponse]
    total: int
    skip: int
    limit: int
