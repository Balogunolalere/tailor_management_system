from sqlalchemy import Column, Integer, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Measurement(Base):
    __tablename__ = "measurements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    measurements = Column(JSON)
    version = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    history = relationship("MeasurementHistory", back_populates="measurement")

    user = relationship("User", back_populates="measurements")

class MeasurementHistory(Base):
    __tablename__ = "measurement_history"

    id = Column(Integer, primary_key=True, index=True)
    measurement_id = Column(Integer, ForeignKey("measurements.id"))
    measurements = Column(JSON)
    version = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    measurement = relationship("Measurement", back_populates="history")

