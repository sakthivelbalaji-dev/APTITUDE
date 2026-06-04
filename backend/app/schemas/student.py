from datetime import datetime
from pydantic import BaseModel, Field


class StudentRegisterRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    department: str = Field(..., min_length=1, max_length=255)
    roll_number: str = Field(..., min_length=1, max_length=100)


class StudentResponse(BaseModel):
    id: int
    name: str
    department: str
    roll_number: str
    resume_path: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True
