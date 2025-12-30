from pydantic import BaseModel
from datetime import date, time
from typing import List


class FeedbackBase(BaseModel):
    fb_date: date
    fb_time: time
    is_neg: bool | None
    fb_desc: str | None
    use_log: List[str] | None


class FeedbackCreate(FeedbackBase):
    pass


class FeedbackResponse(FeedbackBase):
    fb_id: int
    bot_id: int

    class Config:
        from_attributes = True  # Allows Pydantic to read data from database models
