class DomainError(Exception):
    """Base domain exception."""


class NotFoundError(DomainError):
    """Raised when an entity does not exist."""


class ValidationError(DomainError):
    """Raised when business rules fail."""

