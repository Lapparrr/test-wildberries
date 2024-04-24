from collections.abc import Iterable
from operator import and_

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Memory, Photo, User
from app.schemas.requests import MemoryCreateRequest, MemoryUpdateRequest


class PostgresOrm:

    @staticmethod
    async def get_other_memories(session: AsyncSession, current_user: User) -> Iterable:
        data = await session.execute(select(Memory).where(current_user.user_id != Memory.user_id))
        responses = data.unique().scalars()
        return responses

    @staticmethod
    async def get_memories(session: AsyncSession, current_user: User) -> Iterable:
        data = await session.execute(
            select(Memory).where(current_user.user_id == Memory.user_id)
        )
        return data.unique().scalars()

    @staticmethod
    async def get_memory(session: AsyncSession, memory_id: int) -> Iterable | None:
        data = await session.execute(
            select(Memory).where(Memory.id == memory_id)
        )
        return data.scalars().first()

    @staticmethod
    async def set_memory(session: AsyncSession, current_user: User, memory: MemoryCreateRequest) -> bool:
        photos = None
        if memory.photos:
            photos = [Photo(user_id=current_user.user_id, photo_url=str(photo)) for photo in memory.photos]
        data = Memory(
            user_id=current_user.user_id,
            header=memory.header,
            text=memory.text,
            photos=photos
        )
        session.add(data)
        await session.commit()
        return True

    @staticmethod
    async def delete_memory(session: AsyncSession, current_user: User, memory_id: int):
        await session.execute(delete(Memory).where(
            and_(
                Memory.user_id == current_user.user_id,
                Memory.id == memory_id,
            )
        )
        )
        await session.commit()

    @staticmethod
    async def update_memory(session: AsyncSession, current_user: User, memory: MemoryUpdateRequest):
        await session.execute(update(Memory).where(and_(
            Memory.user_id == current_user.user_id,
            Memory.id == memory.id,
        )
        ).values(text=memory.text, header=memory.header)
                              )
        if memory.photos:
            for photo in memory.photos:
                await session.execute(update(Photo).where(and_(
                    Photo.id == photo.id,
                    Photo.user_id == current_user.user_id,
                )
                ).values(photo_url=str(photo.photo_url))
                )
        await session.commit()
