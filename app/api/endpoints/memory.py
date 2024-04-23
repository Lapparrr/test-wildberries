from fastapi import APIRouter, Depends
from sqlalchemy import and_, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import Memory, Photo, User
from app.schemas.requests import MemoryCreateRequest, MemoryUpdateRequest
from app.schemas.responses import MemoryResponse

router = APIRouter()


@router.get('/other/')
async def get_other_memories(
        current_user: User = Depends(deps.get_current_user),
        session: AsyncSession = Depends(deps.get_session),
) -> list[MemoryResponse]:
    """
    Метод для просмотра списка воспоминаний всех остальных пользователей
    """
    data = await session.execute(select(Memory).where(current_user.user_id != Memory.user_id))
    responses = data.unique().scalars()
    return [MemoryResponse.from_orm(response) for response in responses]


@router.get('/')
async def get_memories(
        current_user: User = Depends(deps.get_current_user),
        session: AsyncSession = Depends(deps.get_session),
) -> list[MemoryResponse]:
    """
    Метод для просмотра воспоминаний пользователя
    """
    data = await session.execute(select(Memory).where(current_user.user_id == Memory.user_id))
    responses = data.unique().scalars()
    return [MemoryResponse.from_orm(response) for response in responses]


@router.get('/{memory_id}')
async def get_memory(
        memory_id: int,
        current_user: User = Depends(deps.get_current_user),
        session: AsyncSession = Depends(deps.get_session),
) -> MemoryResponse:
    """
    Получение воспоминания по id
    """
    data = await session.execute(
        select(Memory).where(and_(
            Memory.id == memory_id,
            current_user.user_id == Memory.user_id,
        )
        )
    )
    response = data.unique().scalar_one()
    return MemoryResponse.from_orm(response)


@router.post('/')
async def post_memory(
        memory: MemoryCreateRequest,
        current_user: User = Depends(deps.get_current_user),
        session: AsyncSession = Depends(deps.get_session),
) -> None:
    """
    Метод добавления воспоминания для пользователя
    """
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


@router.delete('/{memory_id}')
async def delete_memory(
        memory_id: int,
        current_user: User = Depends(deps.get_current_user),
        session: AsyncSession = Depends(deps.get_session),
) -> None:
    """
    Удаление воспоминания по id
    """

    await session.execute(delete(Memory).where(and_(
        Memory.user_id == current_user.user_id,
        Memory.id == memory_id,
    )
    )
    )
    await session.commit()


@router.put('/')
async def update_memory(
        memory: MemoryUpdateRequest,
        current_user: User = Depends(deps.get_current_user),
        session: AsyncSession = Depends(deps.get_session)
) -> None:
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
