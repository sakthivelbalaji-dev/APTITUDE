from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.student import Student
from app.schemas.student import StudentLoginRequest, StudentLoginResponse, StudentResponse
from app.services.test_service import is_test_completed

router = APIRouter(prefix="/student", tags=["Student"])


@router.post("/login", response_model=StudentLoginResponse)
def student_login(payload: StudentLoginRequest, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.roll_number == payload.roll_number).first()

    if student:
        if is_test_completed(db, student.id):
            return StudentLoginResponse(
                student=StudentResponse.model_validate(student),
                already_completed=True,
                message="You have already attempted the test.",
            )
        student.name = payload.name
        student.department = payload.department
        db.commit()
        db.refresh(student)
        return StudentLoginResponse(
            student=StudentResponse.model_validate(student),
            already_completed=False,
        )

    student = Student(
        name=payload.name,
        department=payload.department,
        roll_number=payload.roll_number,
    )
    db.add(student)
    db.commit()
    db.refresh(student)

    return StudentLoginResponse(
        student=StudentResponse.model_validate(student),
        already_completed=False,
    )
