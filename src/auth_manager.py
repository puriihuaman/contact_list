from exceptions.blocked_user_error import BlockedUserError
from exceptions.duplicate_user_error import DuplicateUserError
from exceptions.user_not_found_error import UserNotFoundError
from models.user import User


class AuthManager:
    __user_id = 1
    __users_db: dict[str, User] = {}

    def __init__(self):
        pass

    @classmethod
    def register_user(cls, user: User) -> None:
        if cls.__verify_existing_user(user.username):
            raise DuplicateUserError(
                "Usuario duplicado",
                f"El nombre de usuario '{user.username}' ya está en uso"
            )

        cls.__users_db[str(cls.__user_id)] = user
        cls.__user_id += 1

    @classmethod
    def login_user(cls, username: str, password: str) -> User:
        user_found = cls.__find_user(username)

        if not user_found:
            raise UserNotFoundError(
                "Datos inválidos",
                f"Usuario o contraseña inválidos. Por favor, intente nuevamente."
            )

        if user_found.is_locked:
            raise BlockedUserError(
                "Usuario bloqueado",
                f"La cuenta del usuario {username} está bloqueada temporalmente."
            )

        if not user_found.verify_password(password):
            raise ValueError("Datos incorrectos. Usuario o contraseña incorrectos.")

        return user_found

    @classmethod
    def lock_user(cls, username: str) -> None:
        """Bloquea la cuenta de un usuario"""
        user_found = cls.__find_user(username)

        if not user_found:
            raise UserNotFoundError(
                "Datos inválidos",
                f"No se encontró un usuario con ese nombre de usuario: {username}"
            )

        user_found.is_locked = True

    @classmethod
    def __verify_existing_user(cls, username: str) -> bool:
        """Verifica si un usuario ya existe en la base de datos"""
        return cls.__find_user(username) is not None

    @classmethod
    def __find_user(cls, username: str) -> User | None:
        return next((user for user in cls.__users_db.values() if user.username.lower() == username.lower()), None)
