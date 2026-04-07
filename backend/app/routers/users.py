from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas import UserResponse, UserUpdate, UsersList, Message
from app.models import User
from app.dependencies import get_current_user
from app.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "",
    response_model=UsersList,
    summary="Get all users",
    description="Get paginated list of all users (admin only)"
)
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Get list of all users with pagination:
    - **skip**: number of records to skip
    - **limit**: maximum number of records to return
    """
    users = await UserService.get_all(db, skip=skip, limit=limit)
    total = await UserService.count(db)
    return {"users": users, "total": total}


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="Get current authenticated user information"
)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current authenticated user details"""
    return current_user


@router.put(
    "/me",
    response_model=UserResponse,
    summary="Update current user",
    description="Update current user's information"
)
async def update_me(
    update_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Update current user:
    - **username**: new username (optional)
    - **email**: new email (optional)
    - **password**: new password (optional)
    """
    # Check if new username is taken
    if update_data.username and update_data.username != current_user.username:
        existing = await UserService.get_by_username(db, update_data.username)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already taken"
            )

    # Check if new email is taken
    if update_data.email and update_data.email != current_user.email:
        existing = await UserService.get_by_email(db, update_data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

    updated_user = await UserService.update(db, current_user, update_data)
    return updated_user


@router.delete(
    "/me",
    response_model=Message,
    summary="Delete current user",
    description="Delete current user account"
)
async def delete_me(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete current user account permanently"""
    await UserService.delete(db, current_user)
    return {"message": "User account deleted successfully"}


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description="Get user information by user ID"
)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get user by ID"""
    user = await UserService.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user
