from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import status

from repository import MemosRepository
from schemas import SMemoAdd, SMemo, SMemeId

router = APIRouter(
    prefix="/memos",
    tags=["Мемы"],
)


@router.get("", response_model=List[SMemo])
async def get_memos(
        page: int = Query(0, ge=0, description="Номер страницы"),
        size: int = Query(20, ge=1, le=100, description="Количество мемов на странице")
) -> list[SMemo]:
    """
    Получить все мемы.

    :param page: Номер страницы
    :param size: Количество мемов на странице
    :return: Список мемов
    """
    skip = page * size
    limit = size
    memos = await MemosRepository.find_all(skip=skip, limit=limit)
    return memos


@router.get("/{meme_id}", response_model=SMemo)
async def get_memo(meme_id: int) -> SMemo:
    """
    Получить конкретный мем по его идентификатору.

    :param meme_id: Идентификатор мема
    :return: Мем или ошибка, если мем не найден
    """
    meme = await MemosRepository.find_one(meme_id)
    if not meme:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Мем не найден"
        )

    return meme


@router.post("", response_model=SMemeId)
async def add_meme(meme: Annotated[SMemoAdd, Depends()]) -> SMemeId:
    """
    Добавить новый мем.

    :param meme: Данные мема
    :return: Идентификатор добавленного мема
    """
    try:
        meme_id = await MemosRepository.add_one(meme)
        return {"ok": True, "meme_id": meme_id}
    except MemosRepository.MemeAlreadyExists:
        print(f"Мем с таким названием уже существует: {e}")

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Мем с таким названием уже существует"
        )
    except Exception as e:
        print(f"Ошибка добавления мема: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка добавления мема"
        )
