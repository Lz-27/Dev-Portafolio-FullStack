# portafolio_27/backend/app/crud/__init__.py
from app.crud.crud_certification import crud_certification
from app.crud.crud_message import crud_message
from app.crud.crud_project import crud_project
from app.crud.crud_user import crud_user

__all__ = ["crud_user", "crud_message", "crud_project", "crud_certification"]
