from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.student import Student
from app.schemas.student import StudentRegisterRequest, StudentLoginRequest, StudentLoginResponse, StudentResponse
from app.services.test_service import is_test_completed
from app.utils.auth import verify_password, get_password_hash, create_access_token

router = APIRouter(prefix="/student", tags=["Student"])


@router.post("/register", response_model=StudentLoginResponse)
def student_register(payload: StudentRegisterRequest, db: Session = Depends(get_db)):
    try:
        existing_student = db.query(Student).filter(Student.roll_number == payload.roll_number).first()
        if existing_student:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student with this roll number already exists"
            )

        hashed_password = get_password_hash(payload.password)
        student = Student(
            name=payload.name,
            department=payload.department,
            roll_number=payload.roll_number,
            password=hashed_password,
        )
        db.add(student)
        db.commit()
        db.refresh(student)

        access_token = create_access_token(data={"sub": student.id, "role": "student"})
        return StudentLoginResponse(
            access_token=access_token,
            student=StudentResponse.model_validate(student),
            already_completed=False,
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        print(f"Registration error: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )


@router.post("/login", response_model=StudentLoginResponse)
def student_login(payload: StudentLoginRequest, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.roll_number == payload.roll_number).first()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid roll number or password"
        )

    if not verify_password(payload.password, student.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid roll number or password"
        )

    if is_test_completed(db, student.id):
        access_token = create_access_token(data={"sub": student.id, "role": "student"})
        return StudentLoginResponse(
            access_token=access_token,
            student=StudentResponse.model_validate(student),
            already_completed=True,
            message="You have already attempted the test.",
        )

    access_token = create_access_token(data={"sub": student.id, "role": "student"})
    return StudentLoginResponse(
        access_token=access_token,
        student=StudentResponse.model_validate(student),
        already_completed=False,
    )
