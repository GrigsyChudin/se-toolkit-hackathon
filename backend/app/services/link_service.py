from typing import Optional
from sqlalchemy import select, func as sql_func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.link import Link
from app.models.tag import Tag
from app.models.associations import link_tags
from app.schemas.link import LinkCreate, LinkUpdate


class LinkService:
    @staticmethod
    async def get_by_id(db: AsyncSession, link_id: int, user_id: int) -> Optional[Link]:
        result = await db.execute(
            select(Link)
            .where(Link.id == link_id, Link.user_id == user_id)
            .options(selectinload(Link.tags))
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all_by_user(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100) -> list[Link]:
        result = await db.execute(
            select(Link)
            .where(Link.user_id == user_id)
            .options(selectinload(Link.tags))
            .order_by(Link.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def count_by_user(db: AsyncSession, user_id: int) -> int:
        result = await db.execute(
            select(sql_func.count(Link.id)).where(Link.user_id == user_id)
        )
        return result.scalar_one()

    @staticmethod
    async def search_by_tags(db: AsyncSession, user_id: int, tag_names: list[str], skip: int = 0, limit: int = 100) -> list[Link]:
        result = await db.execute(
            select(Link)
            .join(link_tags)
            .join(Tag)
            .where(Link.user_id == user_id, Tag.name.in_(tag_names), Tag.user_id == user_id)
            .options(selectinload(Link.tags))
            .order_by(Link.created_at.desc())
            .offset(skip)
            .limit(limit)
            .distinct()
        )
        return result.scalars().all()

    @staticmethod
    async def search_by_query(db: AsyncSession, user_id: int, query: str, skip: int = 0, limit: int = 100) -> list[Link]:
        search_pattern = f"%{query}%"
        result = await db.execute(
            select(Link)
            .where(
                Link.user_id == user_id,
                (Link.title.ilike(search_pattern) |
                 Link.description.ilike(search_pattern) |
                 Link.url.ilike(search_pattern))
            )
            .options(selectinload(Link.tags))
            .order_by(Link.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def create(db: AsyncSession, user_id: int, link_data: LinkCreate) -> Link:
        link = Link(
            url=str(link_data.url),
            title=link_data.title,
            description=link_data.description,
            user_id=user_id
        )
        
        if link_data.tag_ids:
            tags_result = await db.execute(select(Tag).where(Tag.id.in_(link_data.tag_ids)))
            tags = tags_result.scalars().all()
            link.tags = tags
        
        db.add(link)
        await db.flush()
        await db.refresh(link)
        await db.execute(select(Link).where(Link.id == link.id).options(selectinload(Link.tags)))
        return link

    @staticmethod
    async def update(db: AsyncSession, link: Link, update_data: LinkUpdate) -> Link:
        update_dict = update_data.model_dump(exclude_unset=True)
        
        if "tag_ids" in update_dict:
            tag_ids = update_dict.pop("tag_ids")
            if tag_ids is not None:
                tags_result = await db.execute(select(Tag).where(Tag.id.in_(tag_ids)))
                tags = tags_result.scalars().all()
                link.tags = tags
        
        for field, value in update_dict.items():
            if value is not None:
                setattr(link, field, value)
        
        await db.flush()
        await db.refresh(link)
        return link

    @staticmethod
    async def delete(db: AsyncSession, link: Link) -> bool:
        await db.delete(link)
        await db.flush()
        return True
