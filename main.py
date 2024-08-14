from fastapi import FastAPI, Request, status
from contextlib import asynccontextmanager

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

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


app = FastAPI(lifespan=lifespan, title="Мемчики")
app.include_router(memos_router)


# Только для отладки
@app.exception_handler(RequestValidationError)
async def validation_exeption_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )
