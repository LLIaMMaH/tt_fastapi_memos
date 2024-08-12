from typing import Optional

from pydantic import BaseModel, ConfigDict


class SMemoAdd(BaseModel):
    name: str
    description: Optional[str] = None


class SMemo(SMemoAdd):
    id: int

    model_config = ConfigDict(from_attributes=True)


class SMemeId(BaseModel):
    ok: bool = True
    meme_id: int
