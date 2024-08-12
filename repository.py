from sqlalchemy import select

from database import new_session, MemoOrm
from schemas import SMemoAdd, SMemo


class MemosRepository:
    @classmethod
    async def add_one(cls, data: SMemoAdd) -> int:
        async with new_session() as session:
            meme_dict = data.model_dump()

            meme = MemoOrm(**meme_dict)
            session.add(meme)
            await session.flush()
            await session.commit()
            return meme.id

    @classmethod
    async def find_all(cls) -> list[SMemo]:
        async with new_session() as session:
            query = select(MemoOrm)
            result = await session.execute(query)
            memos_models = result.scalars().all()
            memos_schemas = [SMemo.model_validate(meme_model) for meme_model in memos_models]
            return memos_schemas
