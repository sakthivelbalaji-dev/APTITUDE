from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import csv
import io

from app.config import settings
from app.database import get_db
from app.models.result import Result
from app.models.student import Student
from app.schemas.result import DashboardStats, ResultResponse

router = APIRouter(tags=["Results"])


def _result_to_response(result: Result, student: Student) -> ResultResponse:
    return ResultResponse(
        id=result.id,
        student_id=result.student_id,
        student_name=student.name,
        department=student.department,
        roll_number=student.roll_number,
        score=result.score,
        correct_answers=result.correct_answers,
        wrong_answers=result.wrong_answers,
        percentage=result.percentage,
        status=result.status,
        disqualification_reason=result.disqualification_reason,
        submitted_at=result.submitted_at,
        total_questions=30,
        attempt_number=result.attempt_number,
    )


@router.get("/result/{roll_number}", response_model=ResultResponse)
def get_result_by_roll(
    roll_number: str,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.roll_number == roll_number).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Get the latest completed result
    result = db.query(Result).filter(
        Result.student_id == student.id,
        Result.submitted_at.isnot(None)
    ).order_by(Result.submitted_at.desc()).first()
    
    if not result:
        raise HTTPException(status_code=404, detail="Result not found")

    return _result_to_response(result, student)


@router.get("/result/{roll_number}/history", response_model=list[ResultResponse])
def get_student_history(
    roll_number: str,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(Student.roll_number == roll_number).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    results = db.query(Result).filter(
        Result.student_id == student.id,
        Result.submitted_at.isnot(None)
    ).order_by(Result.submitted_at.desc()).all()

    return [_result_to_response(r, student) for r in results]


@router.get("/results", response_model=list[ResultResponse])
def list_results(
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
    search: str | None = None,
    status_filter: str | None = None,
):
    query = db.query(Result, Student).join(Student, Result.student_id == Student.id)
    if search:
        query = query.filter(
            (Student.name.ilike(f"%{search}%"))
            | (Student.roll_number.ilike(f"%{search}%"))
            | (Student.department.ilike(f"%{search}%"))
        )
    if status_filter:
        query = query.filter(Result.status == status_filter.upper())

    rows = query.order_by(Result.submitted_at.desc()).all()
    return [_result_to_response(r, s) for r, s in rows]


@router.get("/results/stats", response_model=DashboardStats)
def dashboard_stats(db: Session = Depends(get_db)):
    total = db.query(Student).count()
    completed = db.query(Result).filter(Result.submitted_at.isnot(None)).count()
    passed = db.query(Result).filter(Result.status == "PASS").count()
    failed = db.query(Result).filter(Result.status == "FAIL").count()
    disqualified = db.query(Result).filter(Result.status == "DISQUALIFIED").count()
    return DashboardStats(
        total_students=total,
        completed_tests=completed,
        passed=passed,
        failed=failed,
        disqualified=disqualified,
    )


@router.get("/results/export")
def export_results_csv(db: Session = Depends(get_db)):
    rows = (
        db.query(Result, Student)
        .join(Student, Result.student_id == Student.id)
        .filter(Result.submitted_at.isnot(None))
        .all()
    )

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Name", "Department", "Roll Number", "Score", "Correct",
        "Wrong", "Percentage", "Status", "Disqualification Reason", "Submitted At",
    ])
    for result, student in rows:
        writer.writerow([
            student.name,
            student.department,
            student.roll_number,
            result.score,
            result.correct_answers,
            result.wrong_answers,
            result.percentage,
            result.status,
            result.disqualification_reason or "",
            result.submitted_at.isoformat() if result.submitted_at else "",
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=results_export.csv"},
    )
