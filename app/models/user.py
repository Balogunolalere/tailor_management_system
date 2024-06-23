from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.sql import func
from app.database import Base
from sqlalchemy.orm import relationship
import enum

class UserType(enum.Enum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    user_type = Column(Enum(UserType), default=UserType.USER)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    contacts = relationship("Contact", back_populates="user")
    created_families = relationship("Family", back_populates="creator")
    family_memberships = relationship("FamilyMember", back_populates="user")
    measurements = relationship("Measurement", back_populates="user")