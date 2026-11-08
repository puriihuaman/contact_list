from uuid import UUID

from exceptions.contact_not_found_error import ContactNotFoundError
from exceptions.duplicate_email_error import DuplicateEmailError
from exceptions.duplicate_phone_error import DuplicatePhoneError
from models.contact import Contact


class Agenda:
    def __init__(self):
        self.__contacts: list[Contact] = []

    def get_contacts(self) -> list[Contact]:
        return self.__contacts.copy()

    def add_contact(self, contact: Contact) -> None:
        if self.__phone_exists(contact.phone):
            raise DuplicatePhoneError(
                "Contacto duplicado",
                f"El teléfono {contact.phone} ya está registrado."
            )

        if self.__email_exists(contact.email):
            raise DuplicateEmailError(
                "Contacto duplicado",
                f"El email {contact.email} ya está registrado."
            )

        self.__contacts.append(contact)

    def delete_contact(self, contact_id: UUID) -> None:
        contact = self.find_by_id(contact_id)

        if not contact:
            raise ContactNotFoundError(
                "Contacto no encontrado",
                "El contacto que intentas eliminar no existe. Por favor, verifique que exista."
            )

        # self.__contacts = [contact for contact in self.__contacts if contact.contact_id != contact_id]
        self.__contacts.remove(contact)

    def validate_new_phone_number(self, old_phone: str, new_phone: str) -> None:
        if new_phone != old_phone and self.__phone_exists(new_phone):
            raise DuplicatePhoneError(
                "Contacto duplicado",
                f"El teléfono {new_phone} ya pertenece a otro contacto."
            )

    def update_contact(self, contact_id: UUID, partial_update: dict) -> None:
        contact = self.find_by_id(contact_id)

        if not contact:
            raise ContactNotFoundError(
                "Contacto no encontrado",
                "El contacto que intentas actualizar no existe. Por favor, verifique que exista."
            )

        if "name" in partial_update or "phone" in partial_update or "email" in partial_update or "category" in partial_update:
            new_phone = partial_update["phone"]

            if new_phone != contact.phone and self.__phone_exists(new_phone):
                raise DuplicatePhoneError(
                    "Contacto duplicado",
                    f"El teléfono {new_phone} ya pertenece a otro contacto."
                )

            new_email = partial_update["email"]

            if new_email != contact.email and self.__email_exists(new_email):
                raise DuplicateEmailError(
                    "Contacto duplicado",
                    f"El email {new_email} ya pertenece a otro contacto."
                )

            new_name = partial_update["name"] if partial_update["name"] is not None else contact.name

            new_category = partial_update["category"] if partial_update["category"] is not None else contact.category

            contact.name = new_name
            contact.phone = new_phone
            contact.email = new_email
            contact.category = new_category

    def __phone_exists(self, phone: str) -> bool:
        return any(contact.phone == phone for contact in self.__contacts)

    def __email_exists(self, email: str) -> bool:
        return any(contact.email == email for contact in self.__contacts)

    def get_contact_by_index(self, index: int) -> Contact | None:
        if 0 <= index < len(self.__contacts):
            return self.__contacts[index]

        return None

    def find_by_id(self, contact_id: UUID) -> Contact | None:
        if not isinstance(contact_id, UUID):
            raise ValueError("El ID debe ser un UUID válido.")

        for contact in self.__contacts:
            if contact.contact_id == contact_id:
                return contact

        return None

    def find_by_name(self, name: str) -> list[Contact]:
        contacts_found = []

        for contact in self.__contacts:
            if name.lower() in contact.name.lower():
                contacts_found.append(contact)

        return contacts_found

    def find_by_email(self, email: str) -> list[Contact]:
        return [contact for contact in self.__contacts if email.lower() in contact.email.lower()]

    def find_by_phone(self, phone: str) -> list[Contact]:
        return [contact for contact in self.__contacts if phone in contact.phone]

    def to_call(self, phone: str) -> Contact | None:
        contact_found = None

        for contact in self.__contacts:
            if contact.phone == phone:
                contact_found = contact
                break

        return contact_found

    def call_contact(self, phone_number: str) -> Contact:
        if not phone_number:
            raise ValueError("El número de teléfono no puede estar vacío.")

        contact = self.to_call(phone_number)

        if contact is None:
            raise ContactNotFoundError(
                "Contacto no encontrado",
                f"No se encontró ningún contacto con el número de teléfono {phone_number}."
            )

        return contact

    def to_dict(self) -> list[dict[str, str]]:
        return [contact.to_dict() for contact in self.__contacts]

    @staticmethod
    def from_dict(data: list[dict[str, str]]) -> Agenda:
        try:
            # contacts = [Contact.from_dict(contact_data) for contact_data in data["agenda"]]
            contacts = [Contact.from_dict(contact_data) for contact_data in data]
            agenda = Agenda()
            agenda.__contacts = contacts

            return agenda
        except KeyError as e:
            raise KeyError(f"Falta la clave requerida en el diccionario: {e}") from e
        except ValueError as e:
            raise ValueError(f"Error en los datos del contacto: {e}") from e
        except TypeError as e:
            raise TypeError(f"Tipo de dato inválido en los datos del contacto: {e}") from e
