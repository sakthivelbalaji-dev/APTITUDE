import random
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.config import settings
from app.database import SessionLocal, get_db
from app.models.student import Student
from app.models.question import Question
from app.models.result import Result
from app.models.answer import Answer


# -------------------------------------------------------------
# Repository Base Class
# -------------------------------------------------------------
class BaseRepository(ABC):
    @abstractmethod
    def get_student_by_roll(self, roll_number: str) -> Optional[Any]:
        pass

    @abstractmethod
    def create_student(self, name: str, department: str, roll_number: str) -> Any:
        pass

    @abstractmethod
    def update_student(self, student_id: int, name: str, department: str) -> Any:
        pass

    @abstractmethod
    def get_student_by_id(self, student_id: int) -> Optional[Any]:
        pass

    @abstractmethod
    def list_students(self, search: Optional[str] = None, department: Optional[str] = None) -> List[Any]:
        pass

    @abstractmethod
    def get_test_questions(self) -> List[Any]:
        pass

    @abstractmethod
    def list_questions(self, difficulty: Optional[str] = None, topic: Optional[str] = None) -> List[Any]:
        pass

    @abstractmethod
    def create_question(self, question_text: str, option_a: str, option_b: str, option_c: str, option_d: str, correct_answer: str, difficulty: str, topic: str) -> Any:
        pass

    @abstractmethod
    def update_question(self, question_id: int, updates: Dict[str, Any]) -> Optional[Any]:
        pass

    @abstractmethod
    def delete_question(self, question_id: int) -> bool:
        pass

    @abstractmethod
    def bulk_import_questions(self, questions: List[Dict[str, Any]]) -> int:
        pass

    @abstractmethod
    def ensure_result_record(self, student_id: int) -> Any:
        pass

    @abstractmethod
    def save_answer(self, student_id: int, question_id: int, selected_option: str) -> Any:
        pass

    @abstractmethod
    def get_answers_by_student(self, student_id: int) -> List[Any]:
        pass

    @abstractmethod
    def calculate_and_submit(self, student_id: int, question_ids: List[int], disqualified: bool = False, disqualification_reason: Optional[str] = None) -> Any:
        pass

    @abstractmethod
    def is_test_completed(self, student_id: int) -> bool:
        pass

    @abstractmethod
    def get_result_by_student_id(self, student_id: int) -> Optional[Any]:
        pass

    @abstractmethod
    def get_result_by_roll_number(self, roll_number: str) -> Optional[Tuple[Any, Any]]:
        pass

    @abstractmethod
    def list_results(self, search: Optional[str] = None, status_filter: Optional[str] = None) -> List[Tuple[Any, Any]]:
        pass

    @abstractmethod
    def dashboard_stats(self) -> Dict[str, int]:
        pass

    @abstractmethod
    def get_completed_results_with_students(self) -> List[Tuple[Any, Any]]:
        pass


# -------------------------------------------------------------
# SQL Repository (SQLAlchemy)
# -------------------------------------------------------------
class SQLRepository(BaseRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_student_by_roll(self, roll_number: str) -> Optional[Student]:
        return self.db.query(Student).filter(Student.roll_number == roll_number).first()

    def create_student(self, name: str, department: str, roll_number: str) -> Student:
        student = Student(name=name, department=department, roll_number=roll_number)
        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)
        return student

    def update_student(self, student_id: int, name: str, department: str) -> Student:
        student = self.db.query(Student).filter(Student.id == student_id).first()
        if student:
            student.name = name
            student.department = department
            self.db.commit()
            self.db.refresh(student)
        return student

    def get_student_by_id(self, student_id: int) -> Optional[Student]:
        return self.db.query(Student).filter(Student.id == student_id).first()

    def list_students(self, search: Optional[str] = None, department: Optional[str] = None) -> List[Student]:
        query = self.db.query(Student)
        if search:
            query = query.filter(
                or_(
                    Student.name.ilike(f"%{search}%"),
                    Student.roll_number.ilike(f"%{search}%")
                )
            )
        if department:
            query = query.filter(Student.department.ilike(f"%{department}%"))
        return query.order_by(Student.created_at.desc()).all()

    def get_test_questions(self) -> List[Question]:
        easy = self.db.query(Question).filter(Question.difficulty == "easy").all()
        medium = self.db.query(Question).filter(Question.difficulty == "medium").all()

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

    def list_questions(self, difficulty: Optional[str] = None, topic: Optional[str] = None) -> List[Question]:
        query = self.db.query(Question)
        if difficulty:
            query = query.filter(Question.difficulty == difficulty.lower())
        if topic:
            query = query.filter(Question.topic.ilike(f"%{topic}%"))
        return query.order_by(Question.id).all()

    def create_question(self, question_text: str, option_a: str, option_b: str, option_c: str, option_d: str, correct_answer: str, difficulty: str, topic: str) -> Question:
        question = Question(
            question=question_text,
            option_a=option_a,
            option_b=option_b,
            option_c=option_c,
            option_d=option_d,
            correct_answer=correct_answer,
            difficulty=difficulty,
            topic=topic
        )
        self.db.add(question)
        self.db.commit()
        self.db.refresh(question)
        return question

    def update_question(self, question_id: int, updates: Dict[str, Any]) -> Optional[Question]:
        question = self.db.query(Question).filter(Question.id == question_id).first()
        if not question:
            return None
        for key, value in updates.items():
            setattr(question, key, value)
        self.db.commit()
        self.db.refresh(question)
        return question

    def delete_question(self, question_id: int) -> bool:
        question = self.db.query(Question).filter(Question.id == question_id).first()
        if not question:
            return False
        self.db.delete(question)
        self.db.commit()
        return True

    def bulk_import_questions(self, questions_data: List[Dict[str, Any]]) -> int:
        count = 0
        for q in questions_data:
            self.db.add(Question(**q))
            count += 1
        self.db.commit()
        return count

    def ensure_result_record(self, student_id: int) -> Result:
        result = self.db.query(Result).filter(Result.student_id == student_id).first()
        if not result:
            result = Result(student_id=student_id, status="IN_PROGRESS")
            self.db.add(result)
            self.db.commit()
            self.db.refresh(result)
        return result

    def save_answer(self, student_id: int, question_id: int, selected_option: str) -> Answer:
        answer = (
            self.db.query(Answer)
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
            self.db.add(answer)
        self.db.commit()
        self.db.refresh(answer)
        return answer

    def get_answers_by_student(self, student_id: int) -> List[Answer]:
        return self.db.query(Answer).filter(Answer.student_id == student_id).all()

    def calculate_and_submit(self, student_id: int, question_ids: List[int], disqualified: bool = False, disqualification_reason: Optional[str] = None) -> Result:
        student = self.get_student_by_id(student_id)
        if not student:
            raise ValueError("Student not found")

        result = self.ensure_result_record(student_id)
        correct = 0
        wrong = 0
        total = len(question_ids)

        for qid in question_ids:
            question = self.db.query(Question).filter(Question.id == qid).first()
            if not question:
                continue
            answer = (
                self.db.query(Answer)
                .filter(Answer.student_id == student_id, Answer.question_id == qid)
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

        self.db.commit()
        self.db.refresh(result)
        return result

    def is_test_completed(self, student_id: int) -> bool:
        result = self.db.query(Result).filter(Result.student_id == student_id).first()
        return result is not None and result.submitted_at is not None

    def get_result_by_student_id(self, student_id: int) -> Optional[Result]:
        return self.db.query(Result).filter(Result.student_id == student_id).first()

    def get_result_by_roll_number(self, roll_number: str) -> Optional[Tuple[Result, Student]]:
        student = self.get_student_by_roll(roll_number)
        if not student:
            return None
        result = self.get_result_by_student_id(student.id)
        if not result:
            return None
        return result, student

    def list_results(self, search: Optional[str] = None, status_filter: Optional[str] = None) -> List[Tuple[Result, Student]]:
        query = self.db.query(Result, Student).join(Student, Result.student_id == Student.id)
        if search:
            query = query.filter(
                or_(
                    Student.name.ilike(f"%{search}%"),
                    Student.roll_number.ilike(f"%{search}%"),
                    Student.department.ilike(f"%{search}%")
                )
            )
        if status_filter:
            query = query.filter(Result.status == status_filter.upper())
        return query.order_by(Result.submitted_at.desc()).all()

    def dashboard_stats(self) -> Dict[str, int]:
        total = self.db.query(Student).count()
        completed = self.db.query(Result).filter(Result.submitted_at.isnot(None)).count()
        passed = self.db.query(Result).filter(Result.status == "PASS").count()
        failed = self.db.query(Result).filter(Result.status == "FAIL").count()
        disqualified = self.db.query(Result).filter(Result.status == "DISQUALIFIED").count()
        return {
            "total_students": total,
            "completed_tests": completed,
            "passed": passed,
            "failed": failed,
            "disqualified": disqualified
        }

    def get_completed_results_with_students(self) -> List[Tuple[Result, Student]]:
        return (
            self.db.query(Result, Student)
            .join(Student, Result.student_id == Student.id)
            .filter(Result.submitted_at.isnot(None))
            .all()
        )

# -------------------------------------------------------------
# Dependency Provider
# -------------------------------------------------------------
def get_repo() -> BaseRepository:
    """Yields the SQL repository interface."""
    db = SessionLocal()
    try:
        yield SQLRepository(db)
    finally:
        db.close()
