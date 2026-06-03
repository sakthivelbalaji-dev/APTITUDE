import random
from datetime import datetime

from sqlalchemy.orm import Session

from app.config import settings
from app.models.answer import Answer
from app.models.question import Question
from app.models.result import Result
from app.models.student import Student


def get_test_questions(db: Session) -> list[Question]:
    easy = db.query(Question).filter(Question.difficulty == "easy").all()
    medium = db.query(Question).filter(Question.difficulty == "medium").all()

    if len(easy) < settings.TEST_EASY_COUNT or len(medium) < settings.TEST_MEDIUM_COUNT:
        raise ValueError(
            f"Not enough questions. Need {settings.TEST_EASY_COUNT} easy and "
            f"{settings.TEST_MEDIUM_COUNT} medium."
        )

    selected_easy = random.sample(easy, settings.TEST_EASY_COUNT)
    selected_medium = random.sample(medium, settings.TEST_MEDIUM_COUNT)
    questions = selected_easy + selected_medium
    random.shuffle(questions)
    return questions


def ensure_result_record(db: Session, student_id: int) -> Result:
    result = db.query(Result).filter(Result.student_id == student_id).first()
    if not result:
        result = Result(student_id=student_id, status="IN_PROGRESS")
        db.add(result)
        db.commit()
        db.refresh(result)
    return result


def save_answer(db: Session, student_id: int, question_id: int, selected_option: str) -> Answer:
    answer = (
        db.query(Answer)
        .filter(Answer.student_id == student_id, Answer.question_id == question_id)
        .first()
    )
    if answer:
        answer.selected_option = selected_option
    else:
        answer = Answer(
            student_id=student_id,
            question_id=question_id,
            selected_option=selected_option,
        )
        db.add(answer)
    db.commit()
    db.refresh(answer)
    return answer


def calculate_and_submit(
    db: Session,
    student: Student,
    question_ids: list[int],
    disqualified: bool = False,
    disqualification_reason: str | None = None,
) -> Result:
    result = ensure_result_record(db, student.id)
    correct = 0
    wrong = 0
    total = len(question_ids)

    for qid in question_ids:
        question = db.query(Question).filter(Question.id == qid).first()
        if not question:
            continue
        answer = (
            db.query(Answer)
            .filter(Answer.student_id == student.id, Answer.question_id == qid)
            .first()
        )
        if answer and answer.selected_option == question.correct_answer:
            correct += 1
        else:
            wrong += 1

    score = correct
    percentage = (correct / total * 100) if total > 0 else 0.0

    if disqualified:
        status = "DISQUALIFIED"
    elif percentage >= settings.PASS_PERCENTAGE:
        status = "PASS"
    else:
        status = "FAIL"

    result.score = score
    result.correct_answers = correct
    result.wrong_answers = wrong
    result.percentage = round(percentage, 2)
    result.status = status
    result.disqualification_reason = disqualification_reason
    result.submitted_at = datetime.utcnow()

    db.commit()
    db.refresh(result)
    return result


def is_test_completed(db: Session, student_id: int) -> bool:
    result = db.query(Result).filter(Result.student_id == student_id).first()
    return result is not None and result.submitted_at is not None
