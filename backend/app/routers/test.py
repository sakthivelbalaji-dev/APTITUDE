from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models.student import Student
from app.schemas.question import QuestionPublicResponse
from app.schemas.test import SaveAnswerRequest, SubmitTestRequest, TestStartRequest, TestStartResponse
from app.schemas.result import ResultResponse
from app.services import test_service

router = APIRouter(prefix="/test", tags=["Test"])

# In-memory session store for question sets per student (resets on server restart)
_test_sessions: dict[int, list[int]] = {}


@router.post("/start", response_model=TestStartResponse)
def start_test(payload: TestStartRequest, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if test_service.is_test_completed(db, student.id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You have already attempted the test.",
        )

    try:
        questions = test_service.get_test_questions(db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    question_ids = [q.id for q in questions]
    _test_sessions[student.id] = question_ids
    test_service.ensure_result_record(db, student.id)

    return TestStartResponse(
        student_id=student.id,
        questions=[QuestionPublicResponse.model_validate(q) for q in questions],
        duration_minutes=settings.TEST_DURATION_MINUTES,
        total_questions=settings.TEST_TOTAL_QUESTIONS,
    )


@router.post("/save-answer")
def save_answer(payload: SaveAnswerRequest, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if test_service.is_test_completed(db, student.id):
        raise HTTPException(status_code=403, detail="Test already submitted")

    test_service.save_answer(
        db, payload.student_id, payload.question_id, payload.selected_option
    )
    return {"message": "Answer saved"}


@router.post("/submit", response_model=ResultResponse)
def submit_test(payload: SubmitTestRequest, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.id == payload.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    if test_service.is_test_completed(db, student.id):
        from app.models.result import Result

        result = db.query(Result).filter(Result.student_id == student.id).first()
        return _result_to_response(result, student)

    question_ids = _test_sessions.get(student.id, [])
    if not question_ids:
        from app.models.answer import Answer

        answers = db.query(Answer).filter(Answer.student_id == student.id).all()
        question_ids = list({a.question_id for a in answers})

    result = test_service.calculate_and_submit(
        db,
        student,
        question_ids,
        disqualified=payload.disqualified,
        disqualification_reason=payload.disqualification_reason,
    )

    _test_sessions.pop(student.id, None)
    return _result_to_response(result, student)


def _result_to_response(result, student) -> ResultResponse:
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
    )
