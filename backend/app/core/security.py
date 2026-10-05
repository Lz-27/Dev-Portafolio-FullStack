"""
core/security.py
────────────────
Funciones de seguridad:
  - Hashing de contraseñas con bcrypt (directo, sin passlib)
  - Creación y verificación de JWT (python-jose)
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
from jose import JWTError, jwt

from app.core.config import settings


# ── Password Hashing ──────────────────────────────────────────────────────────
def hash_password(plain_password: str) -> str:
    """Retorna el hash bcrypt de la contraseña en texto plano."""
    password_bytes = plain_password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Compara la contraseña en texto plano contra el hash almacenado."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )


# ── JWT ───────────────────────────────────────────────────────────────────────
def _create_token(
    subject: str | Any,
    token_type: str,
    expires_delta: timedelta,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    """
    Función privada base para crear tokens JWT.

    Args:
        subject:      Identificador del usuario (normalmente user_id como str).
        token_type:   "access" | "refresh" — almacenado en el claim "type".
        expires_delta: Tiempo hasta expiración del token.
        extra_claims: Claims adicionales opcionales a incluir en el payload.

    Returns:
        JWT firmado como string.
    """
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        "sub": str(subject),
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
    }
    if extra_claims:
        payload.update(extra_claims)

    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_access_token(subject: str | Any) -> str:
    """Crea un JWT de acceso de corta duración (ACCESS_TOKEN_EXPIRE_MINUTES)."""
    return _create_token(
        subject=subject,
        token_type="access",
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )


def create_refresh_token(subject: str | Any) -> str:
    """Crea un JWT de refresco de larga duración (REFRESH_TOKEN_EXPIRE_DAYS)."""
    return _create_token(
        subject=subject,
        token_type="refresh",
        expires_delta=timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    )


def decode_token(token: str) -> dict[str, Any]:
    """
    Decodifica y valida un JWT.

    Returns:
        El payload del token si es válido.

    Raises:
        JWTError: Si el token es inválido, expirado o mal formado.
    """
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])


def verify_access_token(token: str) -> dict[str, Any]:
    """
    Verifica que el token sea válido Y sea de tipo 'access'.

    Raises:
        JWTError: Si el token no es válido o no es de tipo 'access'.
    """
    payload = decode_token(token)
    if payload.get("type") != "access":
        raise JWTError("Token type mismatch: expected 'access'")
    return payload


def verify_refresh_token(token: str) -> dict[str, Any]:
    """
    Verifica que el token sea válido Y sea de tipo 'refresh'.

    Raises:
        JWTError: Si el token no es válido o no es de tipo 'refresh'.
    """
    payload = decode_token(token)
    if payload.get("type") != "refresh":
        raise JWTError("Token type mismatch: expected 'refresh'")
    return payload
