from typing import Optional

from pydantic import BaseModel


class SMemoAdd(BaseModel):
    name: str
    description: Optional[str] = None


class SMemo(SMemoAdd):
    id: int


class SMemeId(BaseModel):
    ok: bool = True
    meme_id: int
