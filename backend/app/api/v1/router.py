"""
api/v1/router.py
────────────────
Router principal de la versión 1 del API.
Agrega todos los sub-routers de los diferentes recursos.
Para agregar un nuevo recurso: importar su router y llamar a api_router.include_router().
"""
from fastapi import APIRouter

from app.api.v1.endpoints import auth, certifications, messages, projects

api_router = APIRouter()

# ── Registrar sub-routers ─────────────────────────────────────────────────────
api_router.include_router(auth.router)
api_router.include_router(messages.router)
api_router.include_router(projects.router)
api_router.include_router(certifications.router)
