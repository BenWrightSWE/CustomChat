from pydantic import BaseModel, field_validator, EmailStr
import uuid


class UserBase(BaseModel):
    first_name: str
    last_name: str
    company: str | None
    email: str
    phone: str | None

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, value):
        if value is not None:
            if not value.isdigit():
                raise ValueError('Phone must contain only digits')
            if len(value) != 10:
                raise ValueError('Phone must be exactly 10 digits')
        return value


class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    company: str | None = None
    phone: str | None = None


class UserResponse(UserBase):
    user_id: uuid.UUID

    class Config:
        from_attributes = True  # Allows Pydantic to read data from database models


class EmailUpdate(BaseModel):
    email: EmailStr
