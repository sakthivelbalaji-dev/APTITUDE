import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.routers import admin, student, test, result, questions, students_admin
from app.seed import seed_database

print("Starting FastAPI...")
print(f"Port: {os.getenv('PORT', '8000')}")
print(f"Database URL configured: {bool(settings.DATABASE_URL)}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_database()
    yield


app = FastAPI(
    title="Capgemini Aptitude Assessment API",
    description="Mobile aptitude test platform for college students",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router)
app.include_router(student.router)
app.include_router(test.router)
app.include_router(result.router)
app.include_router(questions.router)
app.include_router(students_admin.router)


@app.get("/")
def root():
    return {"status": "ok", "service": "capgemini-aptitude-api"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "capgemini-aptitude-api"}
