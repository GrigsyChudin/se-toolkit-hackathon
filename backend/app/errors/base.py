from fastapi import HTTPException, status
from typing import Optional


class AppError(HTTPException):
    """Base error with error code for frontend handling"""
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: Optional[dict] = None
    ):
        self.code = code
        self.message = message
        self.details = details or {}
        super().__init__(
            status_code=status_code,
            detail={
                "code": code,
                "message": message,
                "details": self.details
            }
        )
