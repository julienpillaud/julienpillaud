class DomainError(Exception):
    """Base class for domain exceptions."""


class BadRequestError(DomainError):
    """Domain error for a 400 HTTP status code."""


class ForbiddenError(DomainError):
    """Domain error for a 403 HTTP status code."""


class NotFoundError(DomainError):
    """Domain error for a 404 HTTP status code."""


class ConflictError(DomainError):
    """Domain error for a 409 HTTP status code."""


class UnprocessableEntityError(DomainError):
    """Domain error for a 422 HTTP status code."""
