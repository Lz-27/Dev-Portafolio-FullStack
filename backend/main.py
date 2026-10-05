"""
main.py
────────
Entry point del servidor FastAPI del Portafolio Profesional.

Para levantar el servidor:
    cd backend
    uvicorn main:app --reload --port 8000

Documentación Swagger UI disponible en:
    http://localhost:8000/docs

Documentación ReDoc disponible en:
    http://localhost:8000/redoc
"""
from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_router
from app.core.config import settings
from app.db.database import SessionLocal
from app.db.init_db import init_db

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


# ── Lifespan (startup / shutdown) ─────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Contexto de vida de la aplicación.
    - startup:  inicializa la BD y crea el admin por defecto
    - shutdown: (espacio para cerrar conexiones externas si se necesita)
    """
    logger.info(f"🚀 Iniciando {settings.APP_NAME} v{settings.APP_VERSION} [{settings.ENVIRONMENT}]")
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close()

    yield  # La aplicación corre aquí

    logger.info("🛑 Apagando servidor...")


# ── Aplicación FastAPI ────────────────────────────────────────────────────────
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
## 🚀 API Backend — Portafolio Profesional

Backend desarrollado con **FastAPI** para el portafolio profesional de Ingeniero de Sistemas.

### Recursos disponibles

| Recurso | Descripción | Auth |
|---------|-------------|------|
| `/auth` | Autenticación OAuth2 + JWT | No |
| `/messages` | Formulario de contacto | POST público / GET admin |
| `/projects` | Proyectos del portafolio | GET público / CRUD admin |
| `/certifications` | Certificaciones | GET público / CRUD admin |

### Autenticación
1. Usa el botón **Authorize** con las credenciales del admin
2. O llama a `POST /api/v1/auth/login` y copia el `access_token`
3. Incluye el header: `Authorization: Bearer <token>`
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
    contact={
        "name": "Portafolio API",
        "email": settings.EMAIL_TO,
    },
)


# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
    expose_headers=["X-Total-Count"],
)


# ── Global Exception Handlers ─────────────────────────────────────────────────
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handler global para excepciones no manejadas.
    En producción, no expone el detalle del error para evitar filtrar información sensible.
    """
    logger.error(f"❌ Excepción no manejada: {exc}", exc_info=True)
    detail = str(exc) if settings.DEBUG else "Error interno del servidor"
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": detail},
    )


# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(api_router, prefix="/api/v1")


# ── Health Check ──────────────────────────────────────────────────────────────
@app.get(
    "/api/v1/health",
    tags=["Sistema"],
    summary="Health check",
    description="Verifica que el servidor está funcionando correctamente.",
)
async def health_check() -> dict:
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


@app.get("/", include_in_schema=False)
async def root() -> dict:
    """Raíz redirige a la documentación."""
    return {
        "message": f"Bienvenido a {settings.APP_NAME} v{settings.APP_VERSION}",
        "docs": "/docs",
        "health": "/api/v1/health",
    }
