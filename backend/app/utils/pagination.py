"""
utils/pagination.py
───────────────────
Utilidades genéricas para paginación de respuestas.
"""
from typing import Generic, Sequence, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class PaginatedParams(BaseModel):
    """Parámetros de consulta para paginación."""
    skip: int = Field(0, ge=0, description="Registros a omitir")
    limit: int = Field(20, ge=1, le=100, description="Máximo de registros a retornar")


class PageResponse(BaseModel, Generic[T]):
    """Estructura estándar de respuesta paginada."""
    items: Sequence[T] = Field(..., description="Elementos de la página actual")
    total: int = Field(..., description="Total de registros existentes")
    skip: int = Field(..., description="Registros omitidos")
    limit: int = Field(..., description="Límite por página solicitado")
