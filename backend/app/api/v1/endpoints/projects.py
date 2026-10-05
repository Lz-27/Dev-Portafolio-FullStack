"""
api/v1/endpoints/projects.py
─────────────────────────────
Endpoints CRUD para proyectos del portafolio:
  GET    /projects/         → Listar proyectos (público, con filtros)
  GET    /projects/{id}     → Detalle de proyecto por ID (público)
  GET    /projects/slug/{slug} → Detalle de proyecto por slug (público)
  POST   /projects/         → Crear proyecto (admin)
  PUT    /projects/{id}     → Actualizar proyecto (admin)
  DELETE /projects/{id}     → Soft delete (admin)
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin, get_db
from app.crud.crud_project import crud_project
from app.schemas.project import (
    ProjectCreate,
    ProjectListResponse,
    ProjectResponse,
    ProjectUpdate,
)

router = APIRouter(prefix="/projects", tags=["Proyectos"])


# ── GET /projects/ ───────────────────────────────────────────────────────────
@router.get(
    "/",
    response_model=ProjectListResponse,
    summary="Listar proyectos",
    description=(
        "Retorna proyectos activos del portafolio. "
        "Filtra por categoría: 'frontend', 'fullstack', 'data', 'desktop', 'backend', o 'all'."
    ),
)
async def list_projects(
    skip: int = Query(default=0, ge=0, description="Registros a omitir"),
    limit: int = Query(default=20, ge=1, le=100, description="Máximo de registros"),
    categoria: str | None = Query(default=None, description="Filtrar por categoría"),
    db: Session = Depends(get_db),
) -> ProjectListResponse:
    items, total = crud_project.get_active_multi(
        db,
        skip=skip,
        limit=limit,
        categoria=categoria,
    )
    return ProjectListResponse(items=items, total=total, skip=skip, limit=limit)


# ── GET /projects/slug/{slug} ────────────────────────────────────────────────
@router.get(
    "/slug/{slug}",
    response_model=ProjectResponse,
    summary="Obtener proyecto por slug",
)
async def get_project_by_slug(
    slug: str,
    db: Session = Depends(get_db),
) -> ProjectResponse:
    project = crud_project.get_by_slug(db, slug=slug)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proyecto con slug='{slug}' no encontrado",
        )
    return project


# ── GET /projects/{id} ───────────────────────────────────────────────────────
@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Obtener proyecto por ID",
)
async def get_project(
    project_id: int,
    db: Session = Depends(get_db),
) -> ProjectResponse:
    project = crud_project.get(db, id=project_id)
    if not project or not project.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proyecto con id={project_id} no encontrado",
        )
    return project


# ── POST /projects/ ──────────────────────────────────────────────────────────
@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear proyecto (Admin)",
    description="Crea un nuevo proyecto en el portafolio. Requiere JWT de administrador.",
)
async def create_project(
    project_in: ProjectCreate,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> ProjectResponse:
    # Verificar slug único
    existing = crud_project.get_by_slug(db, slug=project_in.slug)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Ya existe un proyecto con slug='{project_in.slug}'",
        )
    return crud_project.create(db, obj_in=project_in)


# ── PUT /projects/{id} ───────────────────────────────────────────────────────
@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Actualizar proyecto (Admin)",
    description="Actualización parcial (PATCH semántico). Solo los campos enviados se modifican.",
)
async def update_project(
    project_id: int,
    project_in: ProjectUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> ProjectResponse:
    project = crud_project.get(db, id=project_id)
    if not project or not project.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proyecto con id={project_id} no encontrado",
        )
    return crud_project.update(db, db_obj=project, obj_in=project_in)


# ── DELETE /projects/{id} ────────────────────────────────────────────────────
@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar proyecto (Admin)",
    description="Soft delete: el proyecto se desactiva pero no se borra de la BD.",
)
async def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> None:
    project = crud_project.soft_delete(db, id=project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Proyecto con id={project_id} no encontrado",
        )
