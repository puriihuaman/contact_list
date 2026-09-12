from datetime import datetime


class Contact:
    def __init__(self, name: str, phone: str, email: str, category: str):
        self.__name = name
        self.__phone = phone
        self.__email = email
        self.__category = category

        self.__created_at = datetime.now()
        self.__updated_at = datetime.now()

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        self.__name = name
        self.__updated_at = datetime.now()

    @property
    def phone(self) -> str:
        return self.__phone

    @phone.setter
    def phone(self, phone: str) -> None:
        self.__phone = phone
        self.__updated_at = datetime.now()

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, email: str) -> None:
        self.__email = email
        self.__updated_at = datetime.now()

    @property
    def category(self) -> str:
        return self.__category

    @category.setter
    def category(self, category: str) -> None:
        self.__category = category
        self.__updated_at = datetime.now()

    @property
    def created_at(self) -> datetime:
        return self.__created_at

    @property
    def updated_at(self) -> datetime:
        return self.__updated_at
