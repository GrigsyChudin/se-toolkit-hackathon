from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.models.user import User
from app.auth import decode_access_token
from app.services.user_service import UserService
from app.errors import InvalidTokenError, AccountDeactivatedError

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    try:
        payload = decode_access_token(credentials.credentials)
        if payload is None:
            raise InvalidTokenError()
        
        username: str = payload.get("sub")
        if username is None:
            raise InvalidTokenError()
    except InvalidTokenError:
        raise
    except Exception:
        raise InvalidTokenError()

    user = await UserService.get_by_username(db, username)
    if user is None:
        raise InvalidTokenError()
    
    if not user.is_active:
        raise AccountDeactivatedError()
    
    return user
