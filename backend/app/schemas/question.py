from pydantic import BaseModel, Field


class QuestionBase(BaseModel):
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str = Field(..., pattern="^[ABCD]$")
    difficulty: str = Field(..., pattern="^(easy|medium)$")
    topic: str


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(BaseModel):
    question: str | None = None
    option_a: str | None = None
    option_b: str | None = None
    option_c: str | None = None
    option_d: str | None = None
    correct_answer: str | None = Field(None, pattern="^[ABCD]$")
    difficulty: str | None = Field(None, pattern="^(easy|medium)$")
    topic: str | None = None


class QuestionResponse(QuestionBase):
    id: int

    class Config:
        from_attributes = True


class QuestionPublicResponse(BaseModel):
    id: int
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    difficulty: str
    topic: str

    class Config:
        from_attributes = True
