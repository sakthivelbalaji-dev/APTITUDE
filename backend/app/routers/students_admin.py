from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.result import Result
from app.models.student import Student
from app.schemas.result import ResultResponse
from app.schemas.student import StudentResponse
from app.routers.result import _result_to_response

router = APIRouter(prefix="/students", tags=["Students Admin"])


@router.get("", response_model=list[StudentResponse])
def list_students(
    db: Session = Depends(get_db),
    search: str | None = None,
    department: str | None = None,
):
    query = db.query(Student)
    if search:
        query = query.filter(
            (Student.name.ilike(f"%{search}%"))
            | (Student.roll_number.ilike(f"%{search}%"))
        )
    if department:
        query = query.filter(Student.department.ilike(f"%{department}%"))
    return query.order_by(Student.created_at.desc()).all()


@router.get("/{student_id}", response_model=ResultResponse)
def get_student_result(
    student_id: int,
    db: Session = Depends(get_db),
):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    result = db.query(Result).filter(Result.student_id == student_id).first()
    if not result or not result.submitted_at:
        raise HTTPException(status_code=404, detail="No completed result for this student")

    return _result_to_response(result, student)
