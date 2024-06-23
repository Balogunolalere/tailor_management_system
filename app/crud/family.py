from sqlalchemy.orm import Session
from app.models.family import Family, FamilyMember
from app.schemas.family import FamilyCreate, FamilyUpdate, FamilyMemberCreate
from app.models.measurement import Measurement
from app.models.family import FamilyMember as DBFamilyMember  # Import the SQLAlchemy model

def get_family(db: Session, family_id: int):
    return db.query(Family).filter(Family.id == family_id).first()

def get_families_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Family).filter(Family.created_by == user_id).offset(skip).limit(limit).all()

def create_family(db: Session, family: FamilyCreate):
    db_family = Family(**family.dict())
    db.add(db_family)
    db.commit()
    db.refresh(db_family)
    return db_family

def update_family(db: Session, family_id: int, family: FamilyUpdate):
    db_family = get_family(db, family_id)
    if db_family:
        update_data = family.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_family, key, value)
        db.commit()
        db.refresh(db_family)
    return db_family

def delete_family(db: Session, family_id: int):
    db_family = get_family(db, family_id)
    if db_family:
        db.delete(db_family)
        db.commit()
    return db_family

def add_family_member(db: Session, family_member: FamilyMemberCreate):
    db_family_member = DBFamilyMember(
        family_id=family_member.family_id,
        user_id=family_member.user_id
    )
    db.add(db_family_member)
    db.commit()
    db.refresh(db_family_member)
    return db_family_member

def remove_family_member(db: Session, family_id: int, user_id: int):
    db_family_member = db.query(FamilyMember).filter(
        FamilyMember.family_id == family_id,
        FamilyMember.user_id == user_id
    ).first()
    if db_family_member:
        db.delete(db_family_member)
        db.commit()
    return db_family_member

def get_family_measurements(db: Session, family_id: int):
    family = get_family(db, family_id)
    if family:
        member_ids = [member.user_id for member in family.members]
        return db.query(Measurement).filter(Measurement.user_id.in_(member_ids)).all()
    return []