from typing import Annotated

from fastapi import APIRouter, Depends

from repository import MemosRepository
from schemas import SMemoAdd, SMemo, SMemeId

router = APIRouter(
    prefix="/memos",
    tags=["Мемы"],
)


@router.get("")
async def get_memos() -> list[SMemo]:
    memos = await MemosRepository.find_all()
    return memos


@router.post("")
async def add_meme(meme: Annotated[SMemoAdd, Depends()]) -> SMemeId:
    meme_id = await MemosRepository.add_one(meme)
    return {"ok": True, "meme_id": meme_id}
