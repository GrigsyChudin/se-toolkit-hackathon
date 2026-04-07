from typing import Optional
from sqlalchemy import select, func as sql_func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tag import Tag


class TagService:
    @staticmethod
    async def get_by_id(db: AsyncSession, tag_id: int, user_id: int) -> Optional[Tag]:
        result = await db.execute(
            select(Tag).where(Tag.id == tag_id, Tag.user_id == user_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_name(db: AsyncSession, name: str, user_id: int) -> Optional[Tag]:
        result = await db.execute(
            select(Tag).where(Tag.name == name, Tag.user_id == user_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all_by_user(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100) -> list[Tag]:
        result = await db.execute(
            select(Tag).where(Tag.user_id == user_id).order_by(Tag.name).offset(skip).limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def count_by_user(db: AsyncSession, user_id: int) -> int:
        result = await db.execute(
            select(sql_func.count(Tag.id)).where(Tag.user_id == user_id)
        )
        return result.scalar_one()

    @staticmethod
    async def create(db: AsyncSession, user_id: int, tag_data) -> Tag:
        tag = Tag(name=tag_data.name, color=tag_data.color, user_id=user_id)
        db.add(tag)
        await db.flush()
        await db.refresh(tag)
        return tag

    @staticmethod
    async def update(db: AsyncSession, tag: Tag, update_data) -> Tag:
        update_dict = update_data.model_dump(exclude_unset=True)
        for field, value in update_dict.items():
            setattr(tag, field, value)
        await db.flush()
        await db.refresh(tag)
        return tag

    @staticmethod
    async def delete(db: AsyncSession, tag: Tag) -> bool:
        await db.delete(tag)
        await db.flush()
        return True
