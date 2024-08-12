from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_table, delete_table
from router import router as memos_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await delete_table()
    print("База очищена")
    await create_table()
    print("База готова к работе")
    yield
    print("Выключение приложения")


app = FastAPI(lifespan=lifespan)
app.include_router(memos_router)
