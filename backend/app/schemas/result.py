from datetime import datetime
from pydantic import BaseModel


class ResultResponse(BaseModel):
    id: int
    student_id: int
    student_name: str | None = None
    department: str | None = None
    roll_number: str | None = None
    score: int
    correct_answers: int
    wrong_answers: int
    percentage: float
    status: str
    disqualification_reason: str | None = None
    submitted_at: datetime | None = None
    total_questions: int = 30

    class Config:
        from_attributes = True


class DashboardStats(BaseModel):
    total_students: int
    completed_tests: int
    passed: int
    failed: int
    disqualified: int
