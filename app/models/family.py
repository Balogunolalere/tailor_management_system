from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Family(Base):
    __tablename__ = "families"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    created_by = Column(Integer, ForeignKey("users.id"))

    creator = relationship("User", back_populates="created_families")
    members = relationship("FamilyMember", back_populates="family")

class FamilyMember(Base):
    __tablename__ = "family_members"

    id = Column(Integer, primary_key=True, index=True)
    family_id = Column(Integer, ForeignKey("families.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    family = relationship("Family", back_populates="members")
    user = relationship("User", back_populates="family_memberships")