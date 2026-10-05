"""
api/v1/endpoints/auth.py
────────────────────────
Endpoints de autenticación OAuth2 + JWT:
  POST /auth/login           → retorna access_token + refresh_token
  POST /auth/token/refresh   → renueva el access_token
  GET  /auth/me              → info del usuario autenticado
"""
from __future__ import annotations

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.dependencies import get_current_user, get_db
from app.core.security import (
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
)
from app.crud.crud_user import crud_user
from app.schemas.auth import (
    AccessTokenResponse,
    LoginRequest,
    RefreshTokenRequest,
    TokenResponse,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["Autenticación"])


def _build_token_response(user_id: int) -> TokenResponse:
    """Helper interno: construye la respuesta de token para un user_id dado."""
    return TokenResponse(
        access_token=create_access_token(subject=str(user_id)),
        refresh_token=create_refresh_token(subject=str(user_id)),
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


# ── POST /auth/login (OAuth2 form — compatible con Swagger UI) ────────────────
@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login con OAuth2 Password Flow",
    description=(
        "Autentica al usuario con username y contraseña (form data). "
        "Compatible con el flujo estándar OAuth2 y el botón 'Authorize' de Swagger UI."
    ),
)
async def login_oauth2(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> TokenResponse:
    """Login estándar OAuth2 (form-data). Usado por Swagger UI."""
    user = crud_user.authenticate(
        db,
        username=form_data.username,
        password=form_data.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo",
        )
    return _build_token_response(user.id)


# ── POST /auth/login/json (JSON body — cómodo para Postman) ──────────────────
@router.post(
    "/login/json",
    response_model=TokenResponse,
    summary="Login con JSON body",
    description="Autentica al usuario con username y contraseña en JSON. Ideal para Postman.",
)
async def login_json(
    credentials: LoginRequest,
    db: Session = Depends(get_db),
) -> TokenResponse:
    """Login con JSON body. Idéntico a /login pero acepta JSON en lugar de form."""
    user = crud_user.authenticate(
        db,
        username=credentials.username,
        password=credentials.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario inactivo",
        )
    return _build_token_response(user.id)


# ── POST /auth/token/refresh ──────────────────────────────────────────────────
@router.post(
    "/token/refresh",
    response_model=AccessTokenResponse,
    summary="Renovar Access Token",
    description="Usa el refresh token para obtener un nuevo access token sin volver a loguear.",
)
async def refresh_access_token(
    body: RefreshTokenRequest,
    db: Session = Depends(get_db),
) -> AccessTokenResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Refresh token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_refresh_token(body.refresh_token)
        user_id: str | None = payload.get("sub")
        if not user_id:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = crud_user.get(db, id=int(user_id))
    if not user or not user.is_active:
        raise credentials_exception

    return AccessTokenResponse(
        access_token=create_access_token(subject=str(user.id)),
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


# ── GET /auth/me ──────────────────────────────────────────────────────────────
@router.get(
    "/me",
    response_model=UserResponse,
    summary="Perfil del usuario autenticado",
    description="Retorna los datos del usuario actualmente autenticado.",
)
async def get_me(current_user=Depends(get_current_user)) -> UserResponse:
    return current_user
