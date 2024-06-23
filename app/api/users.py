from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud.user import get_users, get_user, update_user, delete_user
from app.schemas.user import UserUpdate, User
from app.api import deps
from app.models.user import UserType

router = APIRouter()

@router.get("/users/me", response_model=User)
def read_current_user(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    return current_user

@router.get("/users/", response_model=List[User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_admin)
):
    users = get_users(db, skip=skip, limit=limit)
    return users

@router.get("/users/{user_id}", response_model=User)
def read_user(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    db_user = get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if current_user.user_type != UserType.ADMIN and current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return db_user

@router.put("/users/{user_id}", response_model=User)
def update_user_endpoint(
    user_id: int,
    user: UserUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user)
):
    if current_user.user_type != UserType.ADMIN and current_user.id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    db_user = update_user(db, user_id=user_id, user=user)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user

@router.delete("/users/{user_id}", response_model=User)
def delete_user_endpoint(
    user_id: int,
    db: Session = Depends(deps.get_db),
    current_admin: User = Depends(deps.get_current_admin)
):
    db_user = delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return db_user