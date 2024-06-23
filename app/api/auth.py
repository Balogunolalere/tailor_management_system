from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.crud.user import get_user_by_email, crud_create_user, authenticate_user
from app.schemas import token
from app.schemas.user import UserCreate, User
from app.api import deps
from app.core import security
from app.core.config import settings
from app.models.user import UserType

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

@router.post("/login", response_model=token.Token)
def login_access_token(
    db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    user = authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/refresh", response_model=token.Token)
def refresh_token(current_user: User = Depends(deps.get_current_user)):
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            current_user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/signup/admin", response_model=User)
def signup_admin(user: UserCreate, db: Session = Depends(deps.get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    # Create admin user
    return crud_create_user(db=db, user=user, user_type=UserType.ADMIN)

@router.post("/signup", response_model=User)
def signup_user(user: UserCreate, db: Session = Depends(deps.get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    # Create regular user
    return crud_create_user(db=db, user=user, user_type=UserType.USER)