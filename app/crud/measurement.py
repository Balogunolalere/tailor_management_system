from sqlalchemy.orm import Session
from app.models.measurement import Measurement, MeasurementHistory
from app.schemas.measurement import MeasurementCreate, MeasurementUpdate

def get_measurement(db: Session, measurement_id: int):
    return db.query(Measurement).filter(Measurement.id == measurement_id).first()

def get_measurements_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Measurement).filter(Measurement.user_id == user_id).offset(skip).limit(limit).all()

def create_measurement(db: Session, measurement: MeasurementCreate):
    db_measurement = Measurement(**measurement.dict(), version=1)
    db.add(db_measurement)
    db.commit()
    db.refresh(db_measurement)
    return db_measurement

def update_measurement(db: Session, measurement_id: int, measurement: MeasurementUpdate):
    db_measurement = get_measurement(db, measurement_id)
    if db_measurement:
        # Create a history entry
        history_entry = MeasurementHistory(
            measurement_id=db_measurement.id,
            measurements=db_measurement.measurements,
            version=db_measurement.version
        )
        db.add(history_entry)

        # Update the measurement
        update_data = measurement.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_measurement, key, value)
        db_measurement.version += 1
        db.commit()
        db.refresh(db_measurement)
    return db_measurement

def get_measurement_history(db: Session, measurement_id: int):
    return db.query(MeasurementHistory).filter(MeasurementHistory.measurement_id == measurement_id).order_by(MeasurementHistory.version.desc()).all()

def delete_measurement(db: Session, measurement_id: int):
    db_measurement = get_measurement(db, measurement_id)
    if db_measurement:
        db.delete(db_measurement)
        db.commit()
    return db_measurement