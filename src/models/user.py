from datetime import datetime
from uuid import UUID, uuid4

from models.agenda import Agenda


class User:
    def __init__(
            self, name: str, lastname: str, username: str, email: str, password: str, is_locked: bool = False,
            user_id: UUID | None = None
    ):
        self.__user_id = user_id if user_id is not None else uuid4()
        self.__name = self.__validate_name(name)
        self.__lastname = self.__validate_lastname(lastname)
        self.__username = self.__validate_username(username)
        self.__email = self.__validate_email(email)
        self.__password = self.__validate_password(password)
        self.__is_locked = is_locked

        self.__agenda = Agenda()

        self.__created_at = datetime.now()
        self.__updated_at = datetime.now()

    @property
    def user_id(self) -> UUID:
        return self.__user_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def lastname(self) -> str:
        return self.__lastname

    @property
    def username(self) -> str:
        return self.__username

    @property
    def email(self) -> str:
        return self.__email

    @property
    def password(self) -> str:
        return self.__password

    @property
    def is_locked(self) -> bool:
        return self.__is_locked

    @is_locked.setter
    def is_locked(self, value: bool) -> None:
        self.__is_locked = value

    @property
    def agenda(self) -> Agenda:
        return self.__agenda

    @property
    def created_at(self) -> datetime:
        return self.__created_at

    @property
    def updated_at(self) -> datetime:
        return self.__updated_at

    @updated_at.setter
    def updated_at(self, value: datetime) -> None:
        self.__updated_at = value

    def verify_password(self, current_password: str) -> bool:
        return self.__password == current_password

    def to_dict(self) -> dict[str, str | bool | list[dict[str, str]]]:
        return {
            "user_id": self.__user_id.hex,
            "name": self.__name,
            "lastname": self.__lastname,
            "username": self.__username,
            "email": self.__email,
            "password": self.__password,
            "is_locked": self.__is_locked,
            "agenda": self.__agenda.to_dict(),
            "created_at": self.__created_at.isoformat(),
            "updated_at": self.__updated_at.isoformat()
        }

    @staticmethod
    def from_dict(data):
        try:
            agenda = Agenda.from_dict(data["agenda"])

            user = User(
                user_id=UUID(data["user_id"]),
                name=data["name"],
                lastname=data["lastname"],
                username=data["username"],
                email=data["email"],
                password=data["password"],
                is_locked=data["is_locked"],
            )
            user.__agenda = agenda
            user.__created_at = datetime.fromisoformat(data["created_at"])
            user.__updated_at = datetime.fromisoformat(data["updated_at"])

            return user

        except KeyError as e:
            raise KeyError(f"Falta la clave requerida en el diccionario: {e}") from e
        except ValueError as e:
            raise ValueError(f"Error en los datos del usuario: {e}") from e
        except TypeError as e:
            raise TypeError(f"Tipo de dato inválido en los datos del usuario: {e}") from e

    @staticmethod
    def __validate_name(name: str) -> str:
        clean_name = name.strip()

        if not clean_name or len(clean_name) < 3:
            raise ValueError("El nombre del usuario debe tener al menos 3 caracteres.")

        return clean_name

    @staticmethod
    def __validate_lastname(lastname: str) -> str:
        clean_lastname = lastname.strip()

        if not clean_lastname or len(clean_lastname) < 3:
            raise ValueError("El apellido del usuario debe tener al menos 3 caracteres.")

        return clean_lastname

    @staticmethod
    def __validate_email(email: str) -> str:
        clean_email = email.strip()

        if not clean_email or len(clean_email) < 12:
            raise ValueError("El correo electrónico del usuario debe tener al menos 12 caracteres.")

        return clean_email

    @staticmethod
    def __validate_username(username: str) -> str:
        clean_username = username.strip()

        if not clean_username or len(clean_username) < 3:
            raise ValueError("El nombre de usuario debe tener al menos 3 caracteres.")

        return clean_username

    @staticmethod
    def __validate_password(password: str) -> str:
        clean_password = password.strip()

        if not clean_password or len(clean_password) < 6:
            raise ValueError(
                "La contraseña debe tener al menos 6 caracteres. Por favor, ingresa una contraseña más segura."
            )

        return clean_password
