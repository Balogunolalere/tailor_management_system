from pydantic import BaseModel, ConfigDict
from datetime import datetime

class ContactBase(BaseModel):
    phone_number: str
    address: str

class ContactCreate(ContactBase):
    user_id: int

class ContactUpdate(ContactBase):
    pass

class Contact(ContactBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
