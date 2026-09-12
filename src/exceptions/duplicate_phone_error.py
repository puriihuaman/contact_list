class DuplicatePhoneError(Exception):
    """Se lanza cuando se intenta registrar o actualizar a un teléfono que ya existe."""

    def __init__(self, message: str, details: str) -> None:
        self._message = message
        self._details = details

    @property
    def message(self):
        return self._message

    @property
    def details(self):
        return self._details
