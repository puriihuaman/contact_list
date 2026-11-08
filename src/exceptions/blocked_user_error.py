class BlockedUserError(Exception):
    """Se lanza cuando se intenta acceder a un usuario que está bloqueado."""

    def __init__(self, message: str, details: str) -> None:
        self._message = message
        self._details = details

    @property
    def message(self):
        return self._message

    @property
    def details(self):
        return self._details
