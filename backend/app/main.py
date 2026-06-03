import os
import sys
import traceback
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import Base, engine
from app.routers import admin, student, test, result, questions, students_admin
from app.seed import seed_database

print("=" * 50)
print("Starting FastAPI...")
print(f"Port: {os.getenv('PORT', '8000')}")
print(f"Database URL configured: {bool(settings.DATABASE_URL)}")
print(f"DATABASE_URL: {settings.DATABASE_URL[:20]}..." if settings.DATABASE_URL else "DATABASE_URL: NOT SET")
print("=" * 50)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("Database tables created successfully")
        
        print("Seeding database...")
        seed_database()
        print("Database seeded successfully")
    except Exception as e:
        print(f"ERROR during database initialization: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        print("Application will start anyway, but database operations may fail")
    
    print("FastAPI application started successfully")
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

app.include_router(admin.router, prefix="/api")
app.include_router(student.router, prefix="/api")
app.include_router(test.router, prefix="/api")
app.include_router(result.router, prefix="/api")
app.include_router(questions.router, prefix="/api")
app.include_router(students_admin.router, prefix="/api")


@app.get("/api")
def api_root():
    return {"status": "ok", "service": "capgemini-aptitude-api"}


@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "capgemini-aptitude-api"}


# Serve static files from frontend build
static_dir = "static"
print(f"Checking for static directory: {static_dir}")
print(f"Static directory exists: {os.path.exists(static_dir)}")
if os.path.exists(static_dir):
    print(f"Static directory contents: {os.listdir(static_dir)}")
    app.mount("/assets", StaticFiles(directory=f"{static_dir}/assets"), name="assets")
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")
else:
    print("WARNING: Static directory not found, frontend will not be served")


# Catch-all route for SPA (must be after static mount)
from fastapi.responses import FileResponse


@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    """Serve index.html for all non-API routes (SPA routing)"""
    # Don't intercept API routes
    if full_path.startswith("api/"):
        return {"detail": "Not Found"}
    
    # Serve index.html for SPA routing
    index_path = f"{static_dir}/index.html"
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"detail": "Not Found"}
