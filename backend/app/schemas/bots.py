from pydantic import BaseModel
import uuid


class BotBase(BaseModel):
    bot_name: str
    bot_desc: str
    color: str
    uses: int


class BotCreate(BotBase):
    pass


class BotUpdate(BotBase):
    pass


class BotResponse(BotBase):
    bot_id: uuid.UUID

    class Config:
        from_attributes = True  # Allows Pydantic to read data from database models
