import json
from uuid import UUID

from pathlib import Path

from models.user import User


class Repository:
    __BASE_DIR = Path(__file__).parents[1]

    def __init__(self, file_name: str = "contacts.json"):
        self.__file_path = (self.__BASE_DIR / "data" / file_name).resolve()

    def save_users(self, users: dict[UUID, User]) -> None:
        try:
            data = {
                "users": [user.to_dict() for user in users.values()]
            }

            with open(self.__file_path, "w", encoding="utf_8") as file:
                json.dump(data, file, ensure_ascii=False, separators=(",", ":"), indent=4)

        except OSError as e:
            # raise ContactStorageError(f"Error: An error occurred while saving contacts: {e}")
            raise OSError(f"Error: An error occurred while saving contacts: {e}")
        except (KeyError, TypeError, ValueError) as e:
            # raise ContactStorageError(f"Error: An error occurred while saving contacts: {e}")
            raise ValueError(f"Error: An error occurred while saving contacts: {e}")

    def load_users(self) -> dict[UUID, User]:
        try:
            with open(self.__file_path, "r", encoding="utf_8") as file:
                data = json.load(file)

                if not isinstance(data, dict):
                    raise ValueError(
                        "Error: The contact file has an incorrect format. Expected a dictionary with a 'users' key.")

                users = [User.from_dict(user_data) for user_data in data["users"]]

                return {user.user_id: user for user in users}

        except OSError as e:
            raise OSError(f"Error: An error occurred while loading contacts: {e}")
        except (KeyError, TypeError, ValueError) as e:
            raise ValueError(f"Error: An error occurred while loading contacts: {e}")
