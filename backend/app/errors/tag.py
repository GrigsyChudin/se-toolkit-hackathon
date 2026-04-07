from app.errors.base import AppError
from fastapi import status
from typing import Optional


class TagAlreadyExistsError(AppError):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="TAG_ALREADY_EXISTS",
            message="Tag already exists"
        )


class TagNotFoundError(AppError):
    def __init__(self, tag_id: Optional[int] = None):
        details = {"tag_id": tag_id} if tag_id else {}
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code="TAG_NOT_FOUND",
            message="Tag not found",
            details=details
        )
