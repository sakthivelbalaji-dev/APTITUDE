from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Answer(Base):
    __tablename__ = "answers"
    __table_args__ = (UniqueConstraint("student_id", "question_id", name="uq_student_question"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), nullable=False)
    question_id: Mapped[int] = mapped_column(ForeignKey("questions.id"), nullable=False)
    selected_option: Mapped[str | None] = mapped_column(String(1), nullable=True)

    student = relationship("Student", back_populates="answers")
