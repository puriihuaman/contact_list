from datetime import datetime

from models.agenda import Agenda


class User:
    def __init__(self, name: str, lastname: str, username: str, email: str, password: str):
        self.__name = name
        self.__lastname = lastname
        self.__username = username
        self.__email = email
        self.__password = password
        self.__is_locked = False

        self.__agenda = Agenda()

        self.__created_at = datetime.now()
        self.__updated_at = datetime.now()

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

    def verify_password(self, current_password: str) -> bool:
        return self.__password == current_password
