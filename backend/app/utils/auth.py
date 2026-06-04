from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.student import Student

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def get_admin_password_hash() -> str:
    return get_password_hash(settings.ADMIN_PASSWORD)


def authenticate_admin(username: str, password: str) -> bool:
    if username != settings.ADMIN_USERNAME:
        return False
    return password == settings.ADMIN_PASSWORD


async def get_current_admin(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
) -> str:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        username: str | None = payload.get("sub")
        role: str | None = payload.get("role")
        if username is None or role != "admin":
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception


async def get_current_student(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    db: Session = Depends(get_db),
) -> Student:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            credentials.credentials,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        student_id: int | None = payload.get("sub")
        role: str | None = payload.get("role")
        if student_id is None or role != "student":
            raise credentials_exception
        student = db.query(Student).filter(Student.id == student_id).first()
        if student is None:
            raise credentials_exception
        return student
    except JWTError:
        raise credentials_exception
