from typing import cast

from models.contact import Contact
from exceptions.contact_not_found_error import ContactNotFoundError
from exceptions.duplicate_phone_error import DuplicatePhoneError


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

        self.__contacts.append(contact)

    def delete_contact(self, index: int) -> None:
        if not self.__verify_existing_contact_by_index(index):
            raise ContactNotFoundError(
                "Contacto no encontrado",
                "El contacto que intentas eliminar no existe. Por favor, verifique que exista."
            )

        self.__contacts.pop(index)

    def validate_new_phone_number(self, old_phone: str, new_phone: str) -> None:
        if new_phone != old_phone and self.__phone_exists(new_phone):
            raise ValueError(f"El teléfono {new_phone} ya pertenece a otro contacto.")

    def update_contact(self, index: int, new_contact: Contact) -> None:
        if not self.__verify_existing_contact_by_index(index):
            raise ContactNotFoundError(
                "Contacto no encontrado",
                "El contacto que intentas actualizar no existe. Por favor, verifique que exista."
            )

        old_phone = self.__contacts[index].phone
        new_phone = new_contact.phone

        if new_phone != old_phone and self.__phone_exists(new_phone):
            raise DuplicatePhoneError(
                "Contacto duplicado",
                f"El teléfono {new_phone} ya pertenece a otro contacto."
            )

        contact_to_update = cast(Contact, cast(object, new_contact))

        self.__contacts[index] = contact_to_update

    def __phone_exists(self, phone: str) -> bool:
        return any(contact.phone == phone for contact in self.__contacts)

    def __verify_existing_contact_by_index(self, index: int) -> bool:
        return 0 <= index < len(self.__contacts)

    def get_contact_by_index(self, index: int) -> Contact | None:
        if self.__verify_existing_contact_by_index(index):
            return self.__contacts[index]

        raise ContactNotFoundError(
            "Contacto no encontrado",
            "El contacto que intentas obtener no existe. Por favor, verifique que exista."
        )

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

    def call_contact(self, contact_index: int) -> Contact:
        return self.__contacts[contact_index]
