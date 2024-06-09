class SynthientException(Exception):
    """Base class for exceptions in this module."""

    pass


class InternalServerError(SynthientException):
    """Raised when the server returns a 500."""

    pass


class ErrorResponse(SynthientException):
    """Raised when the server returns a 400 or 401."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)
