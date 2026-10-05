"""
api/v1/endpoints/messages.py
─────────────────────────────
Endpoints del formulario de contacto:
  POST   /messages/         → Enviar mensaje (público, con rate limiting)
  GET    /messages/         → Listar mensajes (admin)
  GET    /messages/{id}     → Detalle de un mensaje (admin)
  PUT    /messages/{id}/read → Marcar como leído (admin)
  DELETE /messages/{id}     → Eliminar mensaje (admin)
"""
from __future__ import annotations

import logging

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_admin, get_db
from app.crud.crud_message import crud_message
from app.schemas.message import (
    MessageListResponse,
    MessageCreate,
    MessagePublicResponse,
    MessageReadUpdate,
    MessageResponse,
)
from app.utils.email import send_contact_notification

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/messages", tags=["Mensajes de Contacto"])


# ── POST /messages/ ──────────────────────────────────────────────────────────
@router.post(
    "/",
    response_model=MessagePublicResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Enviar mensaje de contacto",
    description=(
        "Endpoint público para el formulario de contacto del portafolio. "
        "Guarda el mensaje en BD y envía una notificación por email en background. "
        "Rate limit: 5 peticiones por minuto por IP."
    ),
)
async def create_message(
    message_in: MessageCreate,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
) -> MessagePublicResponse:
    """
    Recibe el mensaje del formulario de contacto.

    - Guarda el mensaje en la base de datos.
    - Lanza el envío de email como tarea en background (no bloquea la respuesta).
    - Retorna confirmación al usuario sin exponer datos internos.
    """
    # Capturar IP para auditoría (soporta proxies con X-Forwarded-For)
    client_ip = _get_client_ip(request)

    # Persistir mensaje
    db_message = crud_message.create_with_ip(
        db,
        obj_in=message_in,
        ip_address=client_ip,
    )

    # Notificación por email como tarea en background
    background_tasks.add_task(
        send_contact_notification,
        name=message_in.name,
        email=message_in.email,
        subject=message_in.subject or "Sin asunto",
        message=message_in.message,
        message_id=db_message.id,
    )

    logger.info(f"📧 Nuevo mensaje de contacto id={db_message.id} from={message_in.email}")

    return MessagePublicResponse(id=db_message.id)


# ── GET /messages/ ───────────────────────────────────────────────────────────
@router.get(
    "/",
    response_model=MessageListResponse,
    summary="Listar mensajes (Admin)",
    description="Retorna la lista paginada de mensajes de contacto. Requiere JWT de administrador.",
)
async def list_messages(
    skip: int = 0,
    limit: int = 20,
    unread_only: bool = False,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> MessageListResponse:
    """Lista paginada de mensajes. Solo accesible por administradores."""
    _validate_pagination(skip, limit)
    items, total = crud_message.get_multi_ordered(
        db,
        skip=skip,
        limit=limit,
        unread_only=unread_only,
    )
    return MessageListResponse(items=items, total=total, skip=skip, limit=limit)


# ── GET /messages/{id} ───────────────────────────────────────────────────────
@router.get(
    "/{message_id}",
    response_model=MessageResponse,
    summary="Detalle de un mensaje (Admin)",
)
async def get_message(
    message_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> MessageResponse:
    message = crud_message.get(db, id=message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mensaje con id={message_id} no encontrado",
        )
    return message


# ── PUT /messages/{id}/read ──────────────────────────────────────────────────
@router.put(
    "/{message_id}/read",
    response_model=MessageResponse,
    summary="Marcar mensaje como leído/no leído (Admin)",
)
async def update_message_read(
    message_id: int,
    body: MessageReadUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> MessageResponse:
    message = crud_message.mark_as_read(db, message_id=message_id, is_read=body.is_read)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mensaje con id={message_id} no encontrado",
        )
    return message


# ── DELETE /messages/{id} ────────────────────────────────────────────────────
@router.delete(
    "/{message_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar mensaje (Admin)",
)
async def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(get_current_admin),
) -> None:
    message = crud_message.remove(db, id=message_id)
    if not message:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Mensaje con id={message_id} no encontrado",
        )


# ── Helpers ───────────────────────────────────────────────────────────────────
def _get_client_ip(request: Request) -> str:
    """Extrae la IP real del cliente, soportando proxies y load balancers."""
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "unknown"


def _validate_pagination(skip: int, limit: int) -> None:
    """Valida parámetros de paginación."""
    if skip < 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El parámetro 'skip' debe ser >= 0",
        )
    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="El parámetro 'limit' debe estar entre 1 y 100",
        )
