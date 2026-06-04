import os
import uuid
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.student import Student
from app.schemas.student import StudentRegisterRequest, StudentResponse

router = APIRouter(prefix="/student", tags=["Student"])

# Create uploads directory if it doesn't exist
UPLOAD_DIR = "uploads/resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/register", response_model=StudentResponse)
def student_register(
    name: str,
    department: str,
    roll_number: str,
    resume: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    try:
        existing_student = db.query(Student).filter(Student.roll_number == roll_number).first()
        if existing_student:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student with this roll number already exists"
            )

        # Handle resume upload
        resume_path = None
        if resume:
            # Generate unique filename
            file_extension = os.path.splitext(resume.filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            resume_path = os.path.join(UPLOAD_DIR, unique_filename)
            
            # Save file
            with open(resume_path, "wb") as buffer:
                content = resume.file.read()
                buffer.write(content)

        student = Student(
            name=name,
            department=department,
            roll_number=roll_number,
            resume_path=resume_path,
        )
        db.add(student)
        db.commit()
        db.refresh(student)

        return StudentResponse.model_validate(student)
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
            detail="Registration failed. Please try again."
        )
