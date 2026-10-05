"""
core/config.py
──────────────
Configuración global de la aplicación cargada desde variables de entorno.
Usa Pydantic BaseSettings para validación automática y type-safety.
"""
from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Configuración centralizada del sistema.
    Todos los valores se cargan desde .env (o variables de entorno del SO).
    """

    # ── App ──────────────────────────────────────────────────────────────────
    APP_NAME: str = "Portafolio API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"

    # ── Seguridad / JWT ───────────────────────────────────────────────────────
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # ── Base de Datos ─────────────────────────────────────────────────────────
    DATABASE_URL: str = "sqlite:///./portafolio.db"

    # ── CORS ──────────────────────────────────────────────────────────────────
    CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: Any) -> list[str]:
        """Permite que CORS_ORIGINS venga como JSON string desde .env."""
        if isinstance(value, str):
            return json.loads(value)
        return value

    # ── Email ─────────────────────────────────────────────────────────────────
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAIL_FROM: str = ""
    EMAIL_TO: str = ""

    # ── Admin inicial (seed) ──────────────────────────────────────────────────
    FIRST_ADMIN_USERNAME: str = "admin"
    FIRST_ADMIN_EMAIL: str = "admin@portafolio.com"
    FIRST_ADMIN_PASSWORD: str = "Admin123!"

    # ── Rate Limiting ─────────────────────────────────────────────────────────
    RATE_LIMIT_MESSAGES: str = "5/minute"  # máx peticiones al endpoint de contacto

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Retorna la instancia singleton de Settings.
    El decorador @lru_cache garantiza que el .env se lee una sola vez.
    """
    return Settings()


# Instancia global accesible desde cualquier módulo
settings: Settings = get_settings()
