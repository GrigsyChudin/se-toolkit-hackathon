from app.errors.base import AppError
from fastapi import status
from typing import Optional


class LinkNotFoundError(AppError):
    def __init__(self, link_id: Optional[int] = None):
        details = {"link_id": link_id} if link_id else {}
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            code="LINK_NOT_FOUND",
            message="Link not found",
            details=details
        )


class InvalidTagError(AppError):
    def __init__(self, message: str = "At least one tag is required"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            code="LINK_INVALID_TAGS",
            message=message
        )
