from app.errors.base import AppError
from app.errors.auth import (
    UsernameAlreadyExistsError,
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    AccountDeactivatedError,
    InvalidTokenError,
)
from app.errors.user import UserNotFoundError
from app.errors.tag import TagAlreadyExistsError, TagNotFoundError
from app.errors.link import LinkNotFoundError, InvalidTagError
from app.errors.common import (
    UnauthorizedError,
    ForbiddenError,
    ValidationError,
    InternalServerError,
)

__all__ = [
    "AppError",
    "UsernameAlreadyExistsError",
    "EmailAlreadyExistsError",
    "InvalidCredentialsError",
    "AccountDeactivatedError",
    "InvalidTokenError",
    "UserNotFoundError",
    "TagAlreadyExistsError",
    "TagNotFoundError",
    "LinkNotFoundError",
    "InvalidTagError",
    "UnauthorizedError",
    "ForbiddenError",
    "ValidationError",
    "InternalServerError",
]
