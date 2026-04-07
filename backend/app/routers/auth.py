from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.schemas.auth import UserCreate, UserLogin, Token, UserResponse
from app.auth import verify_password, create_access_token
from app.services.user_service import UserService
from app.dependencies.dependencies import get_current_user
from app.models.user import User
from app.errors import (
    UsernameAlreadyExistsError,
    EmailAlreadyExistsError,
    InvalidCredentialsError,
    AccountDeactivatedError
)
from datetime import timedelta
from app.config import get_settings

router = APIRouter(
    prefix="/auth",
    tags=["1. Authentication"],
    responses={401: {"description": "Unauthorized"}}
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Create a new user account with username, email, and password"
)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    existing_user = await UserService.get_by_username(db, user_data.username)
    if existing_user:
        raise UsernameAlreadyExistsError()

    existing_email = await UserService.get_by_email(db, user_data.email)
    if existing_email:
        raise EmailAlreadyExistsError()

    new_user = await UserService.create(db, user_data)
    return new_user


@router.post(
    "/login",
    response_model=Token,
    summary="Login user",
    description="Authenticate with username and password to get JWT token"
)
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    user = await UserService.get_by_username(db, user_data.username)
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise InvalidCredentialsError()

    if not user.is_active:
        raise AccountDeactivatedError()

    settings = get_settings()
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="Get current authenticated user information"
)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post(
    "/refresh",
    response_model=Token,
    summary="Refresh token",
    description="Get a new token using existing valid token"
)
async def refresh_token(current_user: User = Depends(get_current_user)):
    """
    Refresh the access token using a valid token.
    
    Returns a new JWT token with updated expiration time.
    """
    settings = get_settings()
    access_token = create_access_token(
        data={"sub": current_user.username},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}
