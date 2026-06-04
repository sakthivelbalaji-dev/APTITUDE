from datetime import datetime
from pydantic import BaseModel, Field


class StudentRegisterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    department: str = Field(..., min_length=1, max_length=255)
    roll_number: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=1, max_length=72)


class StudentLoginRequest(BaseModel):
    roll_number: str = Field(..., min_length=1, max_length=100)
    password: str = Field(..., min_length=1, max_length=72)


class StudentResponse(BaseModel):
    id: int
    name: str
    department: str
    roll_number: str
    created_at: datetime

    class Config:
        from_attributes = True


class StudentLoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    student: StudentResponse
    already_completed: bool = False
    message: str | None = None
