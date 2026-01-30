from pydantic import BaseModel
import uuid


class BotBase(BaseModel):
    bot_name: str
    bot_desc: str
    avatar: str
    color: str
    storage: int
    uses: int


class BotCreate(BotBase):
    pass


class BotUpdate(BaseModel):
    bot_name: str | None = None
    bot_desc: str | None = None
    avatar: str | None = None
    color: str | None = None
    storage: int | None = None
    uses: int | None = None


class BotResponse(BotBase):
    bot_id: int

    class Config:
        from_attributes = True  # Allows Pydantic to read data from database models
