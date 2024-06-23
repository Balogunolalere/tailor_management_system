from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.crud.contact import get_contacts_by_user, get_contact, create_contact, update_contact, delete_contact
from app.schemas.contact import ContactCreate, ContactUpdate, Contact
from app.schemas.user import User
from app.api import deps

router = APIRouter()

@router.post("/contacts/", response_model=Contact)
def create__contact(
    contact: ContactCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    return create_contact(db=db, contact=contact)

@router.get("/contacts/", response_model=List[Contact])
def read_contacts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    contacts = get_contacts_by_user(db, user_id=current_user.id, skip=skip, limit=limit)
    return contacts

@router.get("/contacts/{contact_id}", response_model=Contact)
def read_contact(
    contact_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    db_contact = get_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    if db_contact.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this contact")
    return db_contact

@router.put("/contacts/{contact_id}", response_model=Contact)
def update__contact(
    contact_id: int,
    contact: ContactUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    db_contact = get_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    if db_contact.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this contact")
    return update_contact(db, contact_id=contact_id, contact=contact)

@router.delete("/contacts/{contact_id}", response_model=Contact)
def delete__contact(
    contact_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    db_contact = get_contact(db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    if db_contact.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this contact")
    return delete_contact(db, contact_id=contact_id)