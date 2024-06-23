from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from app.models.user import UserType

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    user_type: UserType
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }

class UserUpdate(BaseModel):
    email: Optional[EmailStr]
    username: Optional[str]
    password: Optional[str]
    is_active: Optional[bool]
    user_type: Optional[UserType]
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }