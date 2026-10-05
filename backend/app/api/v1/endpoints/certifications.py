"""
api/v1/endpoints/certifications.py
────────────────────────────────────
Endpoints CRUD para certificaciones del portafolio:
  GET    /certifications/     → Listar certificaciones (público)
  GET    /certifications/{id} → Detalle de certificación (público)
  POST   /certifications/     → Crear certificación (admin)
  PUT    /certifications/{id} → Actualizar certificación (admin)
  DELETE /certifications/{id} → Soft delete (admin)
"""
from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin, get_db
from app.crud.crud_certification import crud_certification
from app.schemas.certification import (
    CertificationCreate,
    CertificationListResponse,
    CertificationResponse,
    CertificationUpdate,
)

router = APIRouter(prefix="/certifications", tags=["Certificaciones"])


# ── GET /certifications/ ─────────────────────────────────────────────────────
@router.get(
    "/",
    response_model=CertificationListResponse,
    summary="Listar certificaciones",
    description=(
        "Retorna certificaciones activas del portafolio. "
        "Filtra por categoría: 'data', 'cloud', 'dev', 'other', o 'all'."
    ),
)
async def list_certifications(
    skip: int = Query(default=0, ge=0, description="Registros a omitir"),
    limit: int = Query(default=50, ge=1, le=100, description="Máximo de registros"),
    categoria: str | None = Query(default=None, description="Filtrar por categoría"),
    db: Session = Depends(get_db),
) -> CertificationListResponse:
    items, total = crud_certification.get_active_multi(
        db,
        skip=skip,
        limit=limit,
        categoria=categoria,
    )
    return CertificationListResponse(items=items, total=total, skip=skip, limit=limit)


# ── GET /certifications/{id} ─────────────────────────────────────────────────
@router.get(
    "/{certification_id}",
    response_model=CertificationResponse,
    summary="Obtener certificación por ID",
)
async def get_certification(
    certification_id: int,
    db: Session = Depends(get_db),
) -> CertificationResponse:
    cert = crud_certification.get(db, id=certification_id)
    if not cert or not cert.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Certificación con id={certification_id} no encontrada",
        )
    return cert


# ── POST /certifications/ ────────────────────────────────────────────────────
@router.post(
    "/",
    response_model=CertificationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear certificación (Admin)",
)
async def create_certification(
    cert_in: CertificationCreate,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> CertificationResponse:
    return crud_certification.create(db, obj_in=cert_in)


# ── PUT /certifications/{id} ─────────────────────────────────────────────────
@router.put(
    "/{certification_id}",
    response_model=CertificationResponse,
    summary="Actualizar certificación (Admin)",
    description="Actualización parcial. Solo los campos enviados se modifican.",
)
async def update_certification(
    certification_id: int,
    cert_in: CertificationUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> CertificationResponse:
    cert = crud_certification.get(db, id=certification_id)
    if not cert or not cert.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Certificación con id={certification_id} no encontrada",
        )
    return crud_certification.update(db, db_obj=cert, obj_in=cert_in)


# ── DELETE /certifications/{id} ──────────────────────────────────────────────
@router.delete(
    "/{certification_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar certificación (Admin)",
    description="Soft delete: la certificación se desactiva, no se borra permanentemente.",
)
async def delete_certification(
    certification_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> None:
    cert = crud_certification.soft_delete(db, id=certification_id)
    if not cert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Certificación con id={certification_id} no encontrada",
        )
