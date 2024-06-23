from sqlalchemy.orm import Session
from app.models.contact import Contact
from app.schemas.contact import ContactCreate, ContactUpdate

def get_contact(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()

def get_contacts_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Contact).filter(Contact.user_id == user_id).offset(skip).limit(limit).all()

def create_contact(db: Session, contact: ContactCreate):
    db_contact = Contact(**contact.dict())
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

def update_contact(db: Session, contact_id: int, contact: ContactUpdate):
    db_contact = get_contact(db, contact_id)
    if db_contact:
        update_data = contact.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_contact, key, value)
        db.commit()
        db.refresh(db_contact)
    return db_contact

def delete_contact(db: Session, contact_id: int):
    db_contact = get_contact(db, contact_id)
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact