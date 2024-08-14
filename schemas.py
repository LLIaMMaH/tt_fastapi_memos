from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class SMemoAdd(BaseModel):
    name: str
    description: Optional[str] = ""


class SMemo(SMemoAdd):
    id: int = Field(ge=1)

    model_config = ConfigDict(from_attributes=True)


class SMemeId(BaseModel):
    ok: bool = True
    meme_id: int = Field(ge=1)
