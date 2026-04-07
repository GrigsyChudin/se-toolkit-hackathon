from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database.database import get_db
from app.schemas.link import LinkCreate, LinkUpdate, LinkResponse, LinkList
from app.schemas.common import Message
from app.dependencies.dependencies import get_current_user
from app.models.user import User
from app.services.link_service import LinkService
from app.errors import LinkNotFoundError, InvalidTagError

router = APIRouter(
    prefix="/links",
    tags=["3. Links"],
    responses={401: {"description": "Unauthorized"}}
)


@router.get(
    "",
    response_model=LinkList,
    summary="Get all links",
    description="Get paginated list of current user's links"
)
async def get_links(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    links = await LinkService.get_all_by_user(db, current_user.id, skip=skip, limit=limit)
    total = await LinkService.count_by_user(db, current_user.id)
    return {"links": links, "total": total}


@router.post(
    "",
    response_model=LinkResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add new link",
    description="Add a new link with optional tags"
)
async def create_link(
    link_data: LinkCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    new_link = await LinkService.create(db, current_user.id, link_data)
    return new_link


@router.get(
    "/{link_id}",
    response_model=LinkResponse,
    summary="Get link by ID",
    description="Get link information by ID"
)
async def get_link(
    link_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    link = await LinkService.get_by_id(db, link_id, current_user.id)
    if not link:
        raise LinkNotFoundError(link_id=link_id)
    return link


@router.put(
    "/{link_id}",
    response_model=LinkResponse,
    summary="Update link",
    description="Update link information and tags"
)
async def update_link(
    link_id: int,
    link_data: LinkUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    link = await LinkService.get_by_id(db, link_id, current_user.id)
    if not link:
        raise LinkNotFoundError(link_id=link_id)

    updated_link = await LinkService.update(db, link, link_data)
    return updated_link


@router.delete(
    "/{link_id}",
    response_model=Message,
    summary="Delete link",
    description="Delete a link"
)
async def delete_link(
    link_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    link = await LinkService.get_by_id(db, link_id, current_user.id)
    if not link:
        raise LinkNotFoundError(link_id=link_id)

    await LinkService.delete(db, link)
    return {"message": "Link deleted successfully"}


@router.get(
    "/search/tags",
    response_model=LinkList,
    summary="Search links by tags",
    description="Search links by tag names"
)
async def search_by_tags(
    tags: str = Query(..., description="Comma-separated tag names"),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    tag_list = [tag.strip() for tag in tags.split(",") if tag.strip()]
    if not tag_list:
        raise InvalidTagError()

    links = await LinkService.search_by_tags(db, current_user.id, tag_list, skip=skip, limit=limit)
    return {"links": links, "total": len(links)}


@router.get(
    "/search/query",
    response_model=LinkList,
    summary="Search links by text",
    description="Search links by title, description, or URL"
)
async def search_by_query(
    q: str = Query(..., min_length=1, description="Search query"),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    links = await LinkService.search_by_query(db, current_user.id, q, skip=skip, limit=limit)
    return {"links": links, "total": len(links)}
