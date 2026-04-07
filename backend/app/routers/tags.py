from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_db
from app.schemas.tag import TagCreate, TagResponse, TagList
from app.schemas.common import Message
from app.dependencies.dependencies import get_current_user
from app.models.user import User
from app.services.tag_service import TagService
from app.errors import TagAlreadyExistsError, TagNotFoundError

router = APIRouter(
    prefix="/tags",
    tags=["2. Tags"],
    responses={401: {"description": "Unauthorized"}}
)


@router.get(
    "",
    response_model=TagList,
    summary="Get all tags",
    description="Get paginated list of current user's tags"
)
async def get_tags(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    tags = await TagService.get_all_by_user(db, current_user.id, skip=skip, limit=limit)
    total = await TagService.count_by_user(db, current_user.id)
    return {"tags": tags, "total": total}


@router.post(
    "",
    response_model=TagResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create new tag",
    description="Create a new tag with name and color"
)
async def create_tag(
    tag_data: TagCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    existing = await TagService.get_by_name(db, tag_data.name, current_user.id)
    if existing:
        raise TagAlreadyExistsError()

    new_tag = await TagService.create(db, current_user.id, tag_data)
    return new_tag


@router.get(
    "/{tag_id}",
    response_model=TagResponse,
    summary="Get tag by ID",
    description="Get tag information by ID"
)
async def get_tag(
    tag_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    tag = await TagService.get_by_id(db, tag_id, current_user.id)
    if not tag:
        raise TagNotFoundError(tag_id=tag_id)
    return tag


@router.put(
    "/{tag_id}",
    response_model=TagResponse,
    summary="Update tag",
    description="Update tag name or color"
)
async def update_tag(
    tag_id: int,
    tag_data: TagCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    tag = await TagService.get_by_id(db, tag_id, current_user.id)
    if not tag:
        raise TagNotFoundError(tag_id=tag_id)

    updated_tag = await TagService.update(db, tag, tag_data)
    return updated_tag


@router.delete(
    "/{tag_id}",
    response_model=Message,
    summary="Delete tag",
    description="Delete a tag (links will not be deleted)"
)
async def delete_tag(
    tag_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    tag = await TagService.get_by_id(db, tag_id, current_user.id)
    if not tag:
        raise TagNotFoundError(tag_id=tag_id)

    await TagService.delete(db, tag)
    return {"message": "Tag deleted successfully"}
