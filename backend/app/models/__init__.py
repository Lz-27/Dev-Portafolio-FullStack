# portafolio_27/backend/app/models/__init__.py
# Importar todos los modelos aquí garantiza que SQLAlchemy los registre
# antes de llamar a Base.metadata.create_all()
from app.models.certification import Certification
from app.models.message import Message
from app.models.project import Project
from app.models.user import User

__all__ = ["User", "Message", "Project", "Certification"]
