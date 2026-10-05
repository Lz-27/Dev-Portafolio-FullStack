"""
crud/crud_certification.py
──────────────────────────
CRUD específico para certificaciones del portafolio.
"""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.certification import Certification
from app.schemas.certification import CertificationCreate, CertificationUpdate


class CRUDCertification(CRUDBase[Certification, CertificationCreate, CertificationUpdate]):
    """CRUD para certificaciones del portafolio."""

    def get_active_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 50,
        categoria: str | None = None,
    ) -> tuple[list[Certification], int]:
        """
        Lista certificaciones activas con filtro opcional por categoría.
        Usado en el endpoint público (sin auth).
        """
        query = db.query(Certification).filter(Certification.is_active == True)  # noqa: E712
        if categoria and categoria != "all":
            query = query.filter(Certification.categoria == categoria)

        total = query.count()
        items = query.order_by(Certification.fecha.desc()).offset(skip).limit(limit).all()
        return items, total

    def get_by_categoria(self, db: Session, *, categoria: str) -> list[Certification]:
        """Retorna todas las certificaciones de una categoría específica."""
        return (
            db.query(Certification)
            .filter(
                Certification.categoria == categoria,
                Certification.is_active == True,  # noqa: E712
            )
            .order_by(Certification.fecha.desc())
            .all()
        )

    def soft_delete(self, db: Session, *, id: int) -> Certification | None:
        """Soft delete: marca is_active=False."""
        cert = db.get(Certification, id)
        if cert:
            cert.is_active = False
            db.commit()
            db.refresh(cert)
        return cert


crud_certification = CRUDCertification(Certification)
