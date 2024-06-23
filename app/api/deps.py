from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.crud.user import get_user
from app.schemas.token import TokenPayload
from app.models.user import User, UserType
from app.core.config import settings
from app.database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    user = get_user(db, user_id=token_data.sub)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if hasattr(current_user, 'is_active') and not current_user.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user

def get_current_admin(
    current_user: User = Depends(get_current_active_user),
) -> User:
    if current_user.user_type != UserType.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user