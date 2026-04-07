from app.errors.base import AppError
from fastapi import status


class UsernameAlreadyExistsError(AppError):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="AUTH_USERNAME_EXISTS",
            message="Username already registered"
        )


class EmailAlreadyExistsError(AppError):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="AUTH_EMAIL_EXISTS",
            message="Email already registered"
        )


class InvalidCredentialsError(AppError):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="AUTH_INVALID_CREDENTIALS",
            message="Incorrect username or password"
        )


class AccountDeactivatedError(AppError):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            code="AUTH_ACCOUNT_DEACTIVATED",
            message="User account is deactivated"
        )


class InvalidTokenError(AppError):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code="AUTH_INVALID_TOKEN",
            message="Could not validate credentials"
        )
