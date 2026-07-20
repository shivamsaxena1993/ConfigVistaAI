class RepositoryError(Exception):
    """Base repository exception."""


class EntityNotFoundError(RepositoryError):
    """Raised when an entity cannot be found."""


class DuplicateEntityError(RepositoryError):
    """Raised when attempting to create a duplicate entity."""