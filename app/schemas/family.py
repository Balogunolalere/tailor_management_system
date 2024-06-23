from pydantic import BaseModel, ConfigDict
from typing import List
from typing import Optional

class FamilyBase(BaseModel):
    name: str

class FamilyCreate(FamilyBase):
    created_by: int

class Family(FamilyBase):
    id: int
    created_by: int

    model_config = ConfigDict(from_attributes=True)


class FamilyMemberBase(BaseModel):
    family_id: int
    user_id: int

class FamilyMemberCreate(FamilyMemberBase):
    pass

class FamilyMember(FamilyMemberBase):
    id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class FamilyWithMembers(Family):
    members: List[FamilyMember]


class FamilyUpdate(FamilyBase):
    pass