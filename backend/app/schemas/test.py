from pydantic import BaseModel, Field


class TestStartRequest(BaseModel):
    student_id: int


class TestStartResponse(BaseModel):
    student_id: int
    questions: list
    duration_minutes: int
    total_questions: int


class SaveAnswerRequest(BaseModel):
    student_id: int
    question_id: int
    selected_option: str = Field(..., pattern="^[ABCD]$")


class SubmitTestRequest(BaseModel):
    student_id: int
    disqualified: bool = False
    disqualification_reason: str | None = None
