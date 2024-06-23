from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Dict, Any

class MeasurementBase(BaseModel):
    measurements: Dict[str, Any]

class MeasurementCreate(MeasurementBase):
    user_id: int

class MeasurementUpdate(MeasurementBase):
    pass

class Measurement(MeasurementBase):
    id: int
    user_id: int
    version: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
