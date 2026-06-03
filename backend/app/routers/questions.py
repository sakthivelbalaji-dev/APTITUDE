from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.question import Question
from app.schemas.question import QuestionCreate, QuestionResponse, QuestionUpdate
from app.utils.auth import get_current_admin

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.get("", response_model=list[QuestionResponse])
def list_questions(
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
    difficulty: str | None = None,
    topic: str | None = None,
):
    query = db.query(Question)
    if difficulty:
        query = query.filter(Question.difficulty == difficulty.lower())
    if topic:
        query = query.filter(Question.topic.ilike(f"%{topic}%"))
    return query.order_by(Question.id).all()


@router.post("", response_model=QuestionResponse)
def create_question(
    payload: QuestionCreate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    question = Question(**payload.model_dump())
    db.add(question)
    db.commit()
    db.refresh(question)
    return question


@router.put("/{question_id}", response_model=QuestionResponse)
def update_question(
    question_id: int,
    payload: QuestionUpdate,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(question, key, value)

    db.commit()
    db.refresh(question)
    return question


@router.delete("/{question_id}")
def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    db.delete(question)
    db.commit()
    return {"message": "Question deleted"}


@router.post("/bulk-import", response_model=dict)
def bulk_import_questions(
    questions: list[QuestionCreate],
    db: Session = Depends(get_db),
    _: str = Depends(get_current_admin),
):
    count = 0
    for q in questions:
        db.add(Question(**q.model_dump()))
        count += 1
    db.commit()
    return {"message": f"Imported {count} questions"}
