"""
core/dependencies.py
────────────────────
FastAPI dependencies reutilizables via Depends().
  - get_db           → inyecta sesión de base de datos
  - get_current_user → verifica JWT y retorna el usuario autenticado
  - get_current_admin → igual que anterior pero exige is_admin=True
"""
from __future__ import annotations

from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.security import verify_access_token
from app.db.database import SessionLocal

# Esquema OAuth2: le indica a FastAPI/Swagger dónde obtener el token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# ── Database ──────────────────────────────────────────────────────────────────
def get_db() -> Generator[Session, None, None]:
    """
    Dependency que abre y cierra la sesión de BD por request.
    Garantiza que la sesión siempre se cierra aunque ocurra una excepción.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ── Auth ──────────────────────────────────────────────────────────────────────
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """
    Verifica el JWT de acceso y retorna el usuario activo.

    Raises:
        401 UNAUTHORIZED: token inválido o expirado.
        401 UNAUTHORIZED: usuario inactivo.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_access_token(token)
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Import here to avoid circular imports
    from app.crud.crud_user import crud_user

    user = crud_user.get(db, id=int(user_id))
    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo",
        )
    return user


def get_current_admin(current_user=Depends(get_current_user)):
    """
    Extiende get_current_user verificando que el usuario sea administrador.

    Raises:
        403 FORBIDDEN: usuario autenticado pero sin permisos de admin.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permisos insuficientes. Se requiere rol de administrador.",
        )
    return current_user
