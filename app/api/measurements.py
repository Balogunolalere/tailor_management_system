from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from app.utils.pdf_generator import generate_measurement_pdf
from app.utils.email import send_measurement_email

from app.crud.measurement import create_measurement, get_measurements_by_user, get_measurement, update_measurement, delete_measurement
from app.schemas.measurement import MeasurementCreate, MeasurementUpdate, Measurement
from app.schemas.user import User

from app.api import deps

router = APIRouter()

@router.post("/measurements/", response_model=Measurement)
def create__measurement(
    measurement: MeasurementCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    return create_measurement(db=db, measurement=measurement)

@router.get("/measurements/", response_model=List[Measurement])
def read_measurements(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    measurements = get_measurements_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return measurements

@router.get("/measurements/{measurement_id}", response_model=Measurement)
def read_measurement(
    measurement_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    db_measurement = get_measurement(db, measurement_id=measurement_id)
    if db_measurement is None:
        raise HTTPException(status_code=404, detail="Measurement not found")
    if db_measurement.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this measurement")
    return db_measurement

@router.put("/measurements/{measurement_id}", response_model=Measurement)
def update__measurement(
    measurement_id: int,
    measurement: MeasurementUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    db_measurement = get_measurement(db, measurement_id=measurement_id)
    if db_measurement is None:
        raise HTTPException(status_code=404, detail="Measurement not found")
    if db_measurement.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this measurement")
    return update_measurement(db, measurement_id=measurement_id, measurement=measurement)

@router.delete("/measurements/{measurement_id}", response_model=Measurement)
def delete__measurement(
    measurement_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    db_measurement = get_measurement(db, measurement_id=measurement_id)
    if db_measurement is None:
        raise HTTPException(status_code=404, detail="Measurement not found")
    if db_measurement.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this measurement")
    return delete_measurement(db, measurement_id=measurement_id)

@router.post("/measurements/{measurement_id}/export")
async def export_measurement(
    measurement_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    measurement = get_measurement(db, measurement_id=measurement_id)
    if measurement is None:
        raise HTTPException(status_code=404, detail="Measurement not found")
    if measurement.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to export this measurement")

    pdf_buffer = generate_measurement_pdf(measurement)
    background_tasks.add_task(send_measurement_email, current_user.email, pdf_buffer)

    return {"message": "Measurement report has been sent to your email."}