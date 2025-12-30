from pydantic import BaseModel
import uuid


class UserBase(BaseModel):
    first_name: str
    last_name: str
    company: str | None
    email: str
    phone: str | None


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    company: str | None = None
    email: str | None = None
    phone: str | None = None


class UserResponse(UserBase):
    user_id: uuid.UUID

    class Config:
        from_attributes = True  # Allows Pydantic to read data from database models
