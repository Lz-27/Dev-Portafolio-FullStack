"""
schemas/message.py
──────────────────
Schemas Pydantic para el recurso Message (formulario de contacto).
Patrón: separar schemas por operación (Create, Response, ListResponse).
"""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator


# ── Request ───────────────────────────────────────────────────────────────────
class MessageCreate(BaseModel):
    """Schema para crear un nuevo mensaje (POST /messages/)."""

    name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nombre completo del remitente",
        examples=["Juan Pérez"],
    )
    email: EmailStr = Field(
        ...,
        description="Email válido del remitente",
        examples=["juan@ejemplo.com"],
    )
    subject: str | None = Field(
        default=None,
        max_length=200,
        description="Asunto opcional del mensaje",
        examples=["Propuesta de proyecto freelance"],
    )
    message: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="Contenido del mensaje",
        examples=["Hola, me gustaría discutir una oportunidad de colaboración..."],
    )

    @field_validator("name")
    @classmethod
    def name_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip()

    @field_validator("message")
    @classmethod
    def message_must_not_be_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El mensaje no puede estar vacío")
        return v.strip()


# ── Response ──────────────────────────────────────────────────────────────────
class MessageResponse(BaseModel):
    """Schema de respuesta para un mensaje individual."""

    id: int
    name: str
    email: str
    subject: str | None
    message: str
    is_read: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class MessageListResponse(BaseModel):
    """Schema de respuesta paginada para listado de mensajes."""

    items: list[MessageResponse]
    total: int
    skip: int
    limit: int


class MessageReadUpdate(BaseModel):
    """Schema para marcar un mensaje como leído/no leído."""

    is_read: bool = True


class MessagePublicResponse(BaseModel):
    """
    Respuesta pública al remitente tras enviar el formulario.
    No expone datos internos como is_read o ip_address.
    """

    id: int
    message: str = "Tu mensaje fue recibido correctamente. Te responderé en menos de 24 horas."

    model_config = {"from_attributes": True}
