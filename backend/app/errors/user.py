from app.errors.base import AppError
from fastapi import status


class UserNotFoundError(AppError):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code="USER_NOT_FOUND",
            message="User not found"
        )
