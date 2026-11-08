from datetime import datetime
from uuid import UUID

from exceptions.blocked_user_error import BlockedUserError
from exceptions.duplicate_user_error import DuplicateUserError
from exceptions.user_not_found_error import UserNotFoundError
from models.user import User
from services.repository import Repository


class AuthManager:
    def __init__(self, repository: Repository):
        self.__repository = repository
        self.__users: dict[UUID, User] = self.__repository.load_users()

    def register_user(self, user: User) -> None:
        if self.__verify_existing_user(user.username):
            raise DuplicateUserError(
                "Usuario duplicado",
                f"El nombre de usuario '{user.username}' ya está en uso"
            )

        user.updated_at = datetime.now()
        self.__users[user.user_id] = user
        self.__repository.save_users(self.__users)

    def login_user(self, username: str, password: str) -> User:
        user_found = self.__find_user(username)

        if not user_found:
            raise UserNotFoundError(
                "Usuario no encontrado",
                f"No se encontró un usuario con ese nombre de usuario: {username}"
            )

        if user_found.is_locked:
            raise BlockedUserError(
                "Usuario bloqueado",
                f"La cuenta del usuario {username} está bloqueada temporalmente."
            )

        if not user_found.verify_password(password):
            raise ValueError("Datos incorrectos. Usuario o contraseña incorrectos.")

        return user_found

    def lock_user(self, username: str) -> None:
        """Bloquea la cuenta de un usuario"""
        user_found = self.__find_user(username)

        if not user_found:
            raise UserNotFoundError(
                "Usuario no encontrado",
                f"No se encontró un usuario con ese nombre de usuario: {username}"
            )

        user_found.is_locked = True
        user_found.updated_at = datetime.now()
        self.__users[user_found.user_id] = user_found
        self.__repository.save_users(self.__users)

    def save(self):
        """Guarda los usuarios en el repositorio"""
        self.__repository.save_users(self.__users)

    def __verify_existing_user(self, username: str) -> bool:
        """Verifica si un usuario ya existe en la base de datos"""
        return next((user for user in self.__users.values() if user.username == username), None) is not None

    def __find_user(self, username: str) -> User | None:
        """Encuentra un usuario por su nombre de usuario"""
        # return next((user for user in AuthManager.__users.values() if user.username == username), None)
        for user in self.__users.values():
            if user.username == username:
                return user

        return None
