"""
crud/crud_project.py
────────────────────
CRUD específico para proyectos del portafolio.
"""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    """CRUD para proyectos del portafolio."""

    def get_by_slug(self, db: Session, *, slug: str) -> Project | None:
        """Busca un proyecto por su slug único (útil para URLs amigables)."""
        return (
            db.query(Project)
            .filter(Project.slug == slug, Project.is_active == True)  # noqa: E712
            .first()
        )

    def get_destacados(self, db: Session) -> list[Project]:
        """Retorna los proyectos marcados como destacados."""
        return (
            db.query(Project)
            .filter(Project.destacado == True, Project.is_active == True)  # noqa: E712
            .order_by(Project.created_at.desc())
            .all()
        )

    def get_by_categoria(
        self,
        db: Session,
        *,
        categoria: str,
        skip: int = 0,
        limit: int = 20,
    ) -> tuple[list[Project], int]:
        """Filtra proyectos activos por categoría con paginación."""
        query = (
            db.query(Project)
            .filter(Project.categoria == categoria, Project.is_active == True)  # noqa: E712
        )
        total = query.count()
        items = query.order_by(Project.created_at.desc()).offset(skip).limit(limit).all()
        return items, total

    def get_active_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 20,
        categoria: str | None = None,
    ) -> tuple[list[Project], int]:
        """
        Lista proyectos activos con filtro opcional por categoría.
        Usado en el endpoint público (sin auth).
        """
        query = db.query(Project).filter(Project.is_active == True)  # noqa: E712
        if categoria and categoria != "all":
            query = query.filter(Project.categoria == categoria)

        total = query.count()
        items = query.order_by(Project.destacado.desc(), Project.created_at.desc()).offset(skip).limit(limit).all()
        return items, total

    def soft_delete(self, db: Session, *, id: int) -> Project | None:
        """
        Soft delete: marca is_active=False en lugar de borrar el registro.
        Preserva la integridad histórica del portafolio.
        """
        project = db.get(Project, id)
        if project:
            project.is_active = False
            db.commit()
            db.refresh(project)
        return project


crud_project = CRUDProject(Project)
