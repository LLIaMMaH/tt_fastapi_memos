from sqlalchemy import select

from database import new_session, MemoOrm
from schemas import SMemoAdd, SMemo


class MemosRepository:
    class MemeAlreadyExists(Exception):
        pass

    @classmethod
    async def add_one(cls, data: SMemoAdd) -> int:
        """
        Добавить новый мем.

        :param data: Данные мема.
        :return: Идентификатор добавленного мема.
        """
        async with new_session() as session:
            # Проверка на валидность данных
            if not SMemoAdd.model_validate(data):
                raise ValueError("Невалидные данные мема")

            meme_dict = data.model_dump()

            # Проверка на существование мема с таким названием
            existing_meme = await cls.find_by_name(meme_dict["name"])
            if existing_meme:
                raise ValueError("Мем с таким названием уже существует")

            meme = MemoOrm(**meme_dict)
            session.add(meme)
            await session.flush()
            await session.commit()
            return meme.id

    @classmethod
    async def find_by_name(cls, name: str) -> MemoOrm:
        """
        Найти мем по имени.

        :param name: Имя мема.
        :return: Мем или None, если мем не найден.
        """
        async with new_session() as session:
            query = select(MemoOrm).filter_by(name=name)
            result = await session.execute(query)
            try:
                return next(result.scalars())
            except StopIteration:
                return None

    @classmethod
    async def find_all(cls, skip: int = 0, limit: int = 20) -> list[SMemo]:
        """
        Получить все мемы с постраничной загрузкой.

        :param skip: Количество мемов, которые нужно пропустить.
        :param limit: Количество мемов на странице.
        :return: Список мемов.
        """
        async with new_session() as session:
            query = select(MemoOrm).offset(skip).limit(limit)
            result = await session.execute(query)
            memos_models = result.scalars().all()
            memos_schemas = [SMemo.model_validate(meme_model) for meme_model in memos_models]
            return memos_schemas

    @classmethod
    async def find_one(cls, meme_id: int) -> SMemo:
        """
        Найти конкретный мем по его идентификатору.

        :param meme_id: Идентификатор мема.
        :return: Мем или None, если мем не найден.
        """
        async with new_session() as session:
            query = select(MemoOrm).filter_by(id=meme_id)
            result = await session.execute(query)
            try:
                meme_model = next(result.scalars())
                return SMemo.model_validate(meme_model)
            except StopIteration:
                return None
