from pydantic import BaseModel, EmailStr, create_model
from typing import Optional
from .settings import settings

if settings.username_is_email:
    username_type = EmailStr
else:
    username_type = str

class UserBase(BaseModel):
    username: username_type

class UserCreate(UserBase):
    password: str

class UNUSED_User(UserBase):
    uuid: str
    is_active: bool

    class Config:
        from_attributes=True

class VerificationCode(BaseModel):
    code: str
