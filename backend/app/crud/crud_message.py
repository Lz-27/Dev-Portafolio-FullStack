"""
crud/crud_message.py
────────────────────
CRUD específico para mensajes del formulario de contacto.
"""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.message import Message
from app.schemas.message import MessageCreate, MessageReadUpdate


class CRUDMessage(CRUDBase[Message, MessageCreate, MessageReadUpdate]):
    """CRUD para mensajes del formulario de contacto."""

    def create_with_ip(
        self,
        db: Session,
        *,
        obj_in: MessageCreate,
        ip_address: str | None = None,
    ) -> Message:
        """
        Crea un mensaje capturando la IP del remitente para auditoría.
        La IP se usa para rate limiting y detección de spam, no se expone públicamente.
        """
        db_message = Message(
            name=obj_in.name,
            email=obj_in.email,
            subject=obj_in.subject,
            message=obj_in.message,
            ip_address=ip_address,
            is_read=False,
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message

    def get_unread(self, db: Session) -> list[Message]:
        """Retorna todos los mensajes no leídos, más recientes primero."""
        return (
            db.query(Message)
            .filter(Message.is_read == False)  # noqa: E712
            .order_by(Message.created_at.desc())
            .all()
        )

    def mark_as_read(self, db: Session, *, message_id: int, is_read: bool = True) -> Message | None:
        """Marca un mensaje como leído o no leído."""
        message = db.get(Message, message_id)
        if message:
            message.is_read = is_read
            db.commit()
            db.refresh(message)
        return message

    def count_unread(self, db: Session) -> int:
        """Cuenta el total de mensajes no leídos."""
        return db.query(Message).filter(Message.is_read == False).count()  # noqa: E712

    def get_multi_ordered(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 20,
        unread_only: bool = False,
    ) -> tuple[list[Message], int]:
        """
        Lista mensajes ordenados por fecha descendente.

        Args:
            unread_only: Si True, solo retorna mensajes no leídos.
        """
        query = db.query(Message)
        if unread_only:
            query = query.filter(Message.is_read == False)  # noqa: E712

        total = query.count()
        items = query.order_by(Message.created_at.desc()).offset(skip).limit(limit).all()
        return items, total


crud_message = CRUDMessage(Message)
