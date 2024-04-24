from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models import User
from app.schemas.requests import MemoryCreateRequest, MemoryUpdateRequest
from app.schemas.responses import MemoryResponse
from app.service.postgres import PostgresOrm

router = APIRouter()


@router.get('/other/')
async def get_other_memories(
        current_user: User = Depends(deps.get_current_user),
        session: AsyncSession = Depends(deps.get_session),
) -> list[MemoryResponse]:
    """
    Метод для просмотра списка воспоминаний всех остальных пользователей
    """
    responses = PostgresOrm.get_other_memories(session, current_user)
    return [MemoryResponse.from_orm(response) for response in responses]


@router.get('/')
async def get_memories(
        current_user: User = Depends(deps.get_current_user),
        session: AsyncSession = Depends(deps.get_session),
) -> list[MemoryResponse]:
    """
    Метод для просмотра воспоминаний пользователя
    """
    responses = PostgresOrm.get_memories(session, current_user)
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
    response = PostgresOrm.get_memory(session, current_user, memory_id)
    return MemoryResponse.from_orm(response)


@router.post('/')
async def post_memory(
        memory: MemoryCreateRequest,
        current_user: User = Depends(deps.get_current_user),
        session: AsyncSession = Depends(deps.get_session),
) -> bool:
    """
    Метод добавления воспоминания для пользователя
    """
    return await PostgresOrm.set_memory(session, current_user, memory)


@router.delete('/{memory_id}')
async def delete_memory(
        memory_id: int,
        current_user: User = Depends(deps.get_current_user),
        session: AsyncSession = Depends(deps.get_session),
) -> None:
    """
    Удаление воспоминания по id
    """
    await PostgresOrm.delete_memory(session, current_user, memory_id)


@router.put('/')
async def update_memory(
        memory: MemoryUpdateRequest,
        current_user: User = Depends(deps.get_current_user),
        session: AsyncSession = Depends(deps.get_session)
) -> None:
    await PostgresOrm.update_memory(session, current_user, memory)
