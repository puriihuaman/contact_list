from datetime import datetime
from uuid import UUID, uuid4

from models.category import Category


class Contact:
    def __init__(
            self, name: str, phone: str, email: str, category: Category = Category.OTHER,
            contact_id: UUID | None = None
    ):
        self.__contact_id = contact_id if contact_id is not None else uuid4()
        self.__name = Contact.__validate_name(name)
        self.__phone = Contact.__validate_phone(phone)
        self.__email = Contact.__validate_email(email)
        self.__category = Contact.__validate_category(category)

        self.__created_at = datetime.now()
        self.__updated_at = datetime.now()

    @property
    def contact_id(self) -> UUID:
        return self.__contact_id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        self.__name = Contact.__validate_name(name)

    @property
    def phone(self) -> str:
        return self.__phone

    @phone.setter
    def phone(self, phone: str) -> None:
        self.__phone = Contact.__validate_phone(phone)

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, email: str) -> None:
        self.__email = Contact.__validate_email(email)

    @property
    def category(self) -> Category:
        return self.__category

    @category.setter
    def category(self, category: Category) -> None:
        self.__category = Contact.__validate_category(category)

    @property
    def created_at(self) -> datetime:
        return self.__created_at

    @property
    def updated_at(self) -> datetime:
        return self.__updated_at

    @updated_at.setter
    def updated_at(self, updated_at: datetime) -> None:
        self.__updated_at = updated_at

    def to_dict(self) -> dict[str, str]:
        return {
            "contact_id": self.__contact_id.hex,
            "name": self.__name,
            "phone": self.__phone,
            "email": self.__email,
            "category": self.__category.value,
            "created_at": self.__created_at.isoformat(),
            "updated_at": self.__updated_at.isoformat()
        }

    @staticmethod
    def from_dict(data: dict[str, str]) -> Contact:
        try:
            contact_id = UUID(data["contact_id"])
            name = data["name"]
            phone = data["phone"]
            email = data["email"]
            category = Category(data["category"])
            created_at = datetime.fromisoformat(data["created_at"])
            updated_at = datetime.fromisoformat(data["updated_at"])

            contact = Contact(name, phone, email, category, contact_id)
            contact.__created_at = created_at
            contact.__updated_at = updated_at

            return contact
        except KeyError as e:
            raise KeyError(f"Falta la clave requerida en el diccionario: {e}") from e
        except ValueError as e:
            raise ValueError(f"Error al crear el contacto desde el diccionario: {e}") from e
        except TypeError as e:
            raise TypeError(f"Tipo de dato incorrecto al crear el contacto desde el diccionario: {e}") from e

    @staticmethod
    def __validate_name(value: str) -> str:
        clean_value = value.strip()

        if not clean_value or len(clean_value) < 3:
            raise ValueError("El nombre del contacto debe tener al menos 3 caracteres.")

        return clean_value

    @staticmethod
    def __validate_phone(value: str) -> str:
        clean_value = value.strip()

        if not clean_value or len(clean_value) < 9:
            raise ValueError("El teléfono del contacto debe tener al menos 9 caracteres.")

        return clean_value

    @staticmethod
    def __validate_email(value: str) -> str:
        clean_value = value.strip()

        if not clean_value or len(clean_value) < 12:
            raise ValueError("El correo electrónico del contacto debe tener al menos 12 caracteres.")

        return clean_value

    @staticmethod
    def __validate_category(category: Category) -> Category:
        if not isinstance(category, Category):
            raise ValueError("La categoría del contacto debe ser una instancia de la clase Category.")

        return category
