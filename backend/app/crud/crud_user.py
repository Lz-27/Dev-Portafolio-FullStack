"""
crud/crud_user.py
─────────────────
CRUD específico para el modelo User con operaciones adicionales
como búsqueda por username/email y autenticación.
"""
from __future__ import annotations

from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.auth import UserResponse


class CRUDUser(CRUDBase[User, UserResponse, UserResponse]):
    """Operaciones CRUD extendidas para el modelo User."""

    def get_by_username(self, db: Session, *, username: str) -> User | None:
        """Busca un usuario por su nombre de usuario."""
        return db.query(User).filter(User.username == username).first()

    def get_by_email(self, db: Session, *, email: str) -> User | None:
        """Busca un usuario por su email."""
        return db.query(User).filter(User.email == email).first()

    def create_user(
        self,
        db: Session,
        *,
        username: str,
        email: str,
        password: str,
        is_admin: bool = False,
    ) -> User:
        """
        Crea un usuario hasheando la contraseña antes de persistir.
        Nunca almacena la contraseña en texto plano.
        """
        db_user = User(
            username=username,
            email=email,
            hashed_password=hash_password(password),
            is_admin=is_admin,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def authenticate(
        self,
        db: Session,
        *,
        username: str,
        password: str,
    ) -> User | None:
        """
        Autentica al usuario verificando username y contraseña.

        Returns:
            El objeto User si las credenciales son válidas, None en caso contrario.
        """
        user = self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_admin(self, user: User) -> bool:
        return user.is_admin


crud_user = CRUDUser(User)
