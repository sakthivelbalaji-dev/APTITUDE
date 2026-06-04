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
    # Truncate password to 72 bytes (bcrypt limitation)
    try:
        # Convert to bytes and truncate to exactly 72 bytes
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
            print(f"Password truncated from {len(password.encode('utf-8'))} to 72 bytes")
        # Decode back to string, ignoring any errors
        truncated_password = password_bytes.decode('utf-8', errors='ignore')
        print(f"Hashing password (length: {len(truncated_password)} chars)")
        return pwd_context.hash(truncated_password)
    except Exception as e:
        print(f"Error hashing password: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        # Fallback: use a simple truncation
        truncated = password[:72]
        print(f"Using fallback truncation (length: {len(truncated)} chars)")
        return pwd_context.hash(truncated)


def create_access_token(data: dict) -> str:
    try:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        print(f"Token created successfully for user: {data.get('sub')}")
        return encoded
    except Exception as e:
        print(f"Error creating access token: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create access token"
        )


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
            print(f"Invalid token payload: username={username}, role={role}")
            raise credentials_exception
        print(f"Admin authenticated successfully: {username}")
        return username
    except JWTError as e:
        print(f"JWT error in get_current_admin: {e}")
        raise credentials_exception
    except Exception as e:
        print(f"Unexpected error in get_current_admin: {e}")
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
        sub = payload.get("sub")
        role: str | None = payload.get("role")
        if sub is None or role != "student":
            print(f"Invalid token payload: sub={sub}, role={role}")
            raise credentials_exception
        try:
            student_id = int(sub)
        except (ValueError, TypeError):
            print(f"Invalid student id format in token sub: {sub}")
            raise credentials_exception
        student = db.query(Student).filter(Student.id == student_id).first()
        if student is None:
            print(f"Student not found with id: {student_id}")
            raise credentials_exception
        print(f"Student authenticated successfully: {student.roll_number}")
        return student
    except JWTError as e:
        print(f"JWT error in get_current_student: {e}")
        raise credentials_exception
    except Exception as e:
        print(f"Unexpected error in get_current_student: {e}")
        raise credentials_exception
