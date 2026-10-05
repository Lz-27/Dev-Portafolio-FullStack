"""
schemas/auth.py
───────────────
Schemas Pydantic para autenticación OAuth2 + JWT.
"""
from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field


# ── Request ───────────────────────────────────────────────────────────────────
class LoginRequest(BaseModel):
    """Credenciales para login (alternativa JSON al form de OAuth2)."""

    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)


class RefreshTokenRequest(BaseModel):
    """Token de refresco para obtener un nuevo access token."""

    refresh_token: str


# ── Response ──────────────────────────────────────────────────────────────────
class TokenResponse(BaseModel):
    """Respuesta estándar de autenticación con ambos tokens."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int  # Segundos hasta expiración del access token


class AccessTokenResponse(BaseModel):
    """Respuesta de renovación con solo el access token."""

    access_token: str
    token_type: str = "bearer"
    expires_in: int


# ── User Info ─────────────────────────────────────────────────────────────────
class UserResponse(BaseModel):
    """Información pública del usuario autenticado."""

    id: int
    username: str
    email: str
    is_admin: bool

    model_config = {"from_attributes": True}
