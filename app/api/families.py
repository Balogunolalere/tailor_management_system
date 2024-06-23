from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud.family import create_family, get_families_by_user, get_family, update_family, delete_family, add_family_member, remove_family_member, get_family_measurements
from app.schemas.family import FamilyCreate, FamilyUpdate, Family, FamilyWithMembers, FamilyMember, FamilyMemberCreate
from app.schemas.measurement import Measurement
from app.schemas.user import User
from app.api import deps
from app.crud.user import get_user
from app.schemas.family import FamilyMember as PydanticFamilyMember  # Import the Pydantic model
from app.models.family import FamilyMember as DBFamilyMember  # Import the SQLAlchemy model


router = APIRouter()

@router.post("/families/", response_model=Family)
def create__family(
    family: FamilyCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    family.created_by = current_user.id
    return create_family(db=db, family=family)

@router.get("/families/", response_model=List[Family])
def read_families(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    families = get_families_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return families

@router.get("/families/{family_id}", response_model=FamilyWithMembers)
def read_family(
    family_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    db_family = get_family(db, family_id=family_id)
    if db_family is None:
        raise HTTPException(status_code=404, detail="Family not found")
    if db_family.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this family")
    return db_family

@router.put("/families/{family_id}", response_model=Family)
def update__family(
    family_id: int,
    family: FamilyUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    db_family = get_family(db, family_id=family_id)
    if db_family is None:
        raise HTTPException(status_code=404, detail="Family not found")
    if db_family.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this family")
    return update_family(db, family_id=family_id, family=family)

@router.delete("/families/{family_id}", response_model=Family)
def delete__family(
    family_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    db_family = get_family(db, family_id=family_id)
    if db_family is None:
        raise HTTPException(status_code=404, detail="Family not found")
    if db_family.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this family")
    return delete_family(db, family_id=family_id)

@router.post("/families/{family_id}/members", response_model=PydanticFamilyMember)
def add__family_member(
    family_id: int,
    member: FamilyMemberCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    # Check if the family exists
    db_family = get_family(db, family_id=family_id)
    if db_family is None:
        raise HTTPException(status_code=404, detail="Family not found")
    
    # Check if the current user has permission to add members
    if db_family.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to add members to this family")
    
    # Check if the user to be added exists
    user_to_add = get_user(db, user_id=member.user_id)
    if user_to_add is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if the user is already a member of this family
    existing_member = db.query(DBFamilyMember).filter(
        DBFamilyMember.family_id == family_id,
        DBFamilyMember.user_id == member.user_id
    ).first()
    if existing_member:
        raise HTTPException(status_code=400, detail="User is already a member of this family")
    
    # If all checks pass, add the new family member
    new_member = FamilyMemberCreate(family_id=family_id, user_id=member.user_id)
    db_family_member = add_family_member(db=db, family_member=new_member)
    
    # Convert the SQLAlchemy model instance to a Pydantic model instance
    return PydanticFamilyMember.from_orm(db_family_member)

@router.delete("/families/{family_id}/members/{user_id}", response_model=FamilyMember)
def remove__family_member(
    family_id: int,
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    db_family = get_family(db, family_id=family_id)
    if db_family is None:
        raise HTTPException(status_code=404, detail="Family not found")
    if db_family.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to remove members from this family")
    return remove_family_member(db, family_id=family_id, user_id=user_id)

@router.get("/families/{family_id}/measurements", response_model=List[Measurement])
def get__family_measurements(
    family_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    db_family = get_family(db, family_id=family_id)
    if db_family is None:
        raise HTTPException(status_code=404, detail="Family not found")
    if db_family.created_by != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this family's measurements")
    return get_family_measurements(db, family_id=family_id)
