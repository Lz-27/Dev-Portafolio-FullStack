"""
crud/base.py
────────────
CRUDBase genérico que implementa las operaciones comunes para cualquier modelo.
Las clases CRUD específicas heredan de este y solo agregan lógica particular.

Tipo genérico: ModelType → el modelo SQLAlchemy
               CreateSchemaType → schema Pydantic de creación
               UpdateSchemaType → schema Pydantic de actualización
"""
from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    CRUD genérico reutilizable.

    Uso:
        class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
            pass
        crud_project = CRUDProject(Project)
    """

    def __init__(self, model: type[ModelType]) -> None:
        self.model = model

    # ── Read ──────────────────────────────────────────────────────────────────
    def get(self, db: Session, *, id: int) -> ModelType | None:
        """Obtiene un registro por su PK. Retorna None si no existe."""
        return db.get(self.model, id)

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 20,
        filters: dict[str, Any] | None = None,
    ) -> tuple[list[ModelType], int]:
        """
        Retorna una lista paginada de registros y el total sin paginar.

        Args:
            skip:    Número de registros a omitir (offset).
            limit:   Máximo de registros a retornar.
            filters: Dict de {campo: valor} para filtrar.

        Returns:
            Tupla (items, total_count).
        """
        query = db.query(self.model)

        if filters:
            for field, value in filters.items():
                if value is not None and hasattr(self.model, field):
                    query = query.filter(getattr(self.model, field) == value)

        total = query.count()
        items = query.offset(skip).limit(limit).all()
        return items, total

    # ── Create ────────────────────────────────────────────────────────────────
    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Crea un nuevo registro a partir de un schema Pydantic.
        Serializa listas a JSON si el modelo las espera como strings.
        """
        import json

        obj_data = obj_in.model_dump()

        # Serializar listas a JSON string para SQLite/columnas Text
        for key, value in obj_data.items():
            if isinstance(value, list):
                obj_data[key] = json.dumps(value, ensure_ascii=False)

        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # ── Update ────────────────────────────────────────────────────────────────
    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any],
    ) -> ModelType:
        """
        Actualiza un registro existente con los campos proporcionados.
        Solo actualiza los campos que vienen en obj_in (PATCH semántico).
        """
        import json

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            if hasattr(db_obj, field):
                if isinstance(value, list):
                    value = json.dumps(value, ensure_ascii=False)
                setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    # ── Delete ────────────────────────────────────────────────────────────────
    def remove(self, db: Session, *, id: int) -> ModelType | None:
        """
        Elimina un registro por PK y lo retorna.
        Retorna None si el registro no existe.
        """
        obj = db.get(self.model, id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj
