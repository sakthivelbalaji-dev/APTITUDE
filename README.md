# Capgemini Aptitude Assessment Portal

Mobile-first aptitude test platform for college students with admin management, anti-cheating, and PostgreSQL backend.

## Tech Stack

- **Frontend:** React (Vite) + Tailwind CSS + Axios + React Router
- **Backend:** FastAPI + SQLAlchemy + Alembic + JWT
- **Database:** PostgreSQL
- **Auth:** JWT (Admin only)
- **Deploy:** Docker + Railway

## Features

### Student Portal
- Registration with Name, Department, Roll Number
- 30-question aptitude test (15 easy + 15 medium)
- 30-minute timer with warning indicators
- Real-time answer saving
- Anti-cheating detection:
  - Tab switching detection
  - Screenshot detection (Print Screen)
  - Clipboard monitoring (large text paste, multiple copies)
  - Dev tools detection
  - AI tool usage pattern detection
- Results display with score out of 30, percentage, and status

### Admin Portal
- Secure JWT authentication
- Dashboard with statistics (total students, completed tests, passed, failed, disqualified)
- Student management with search and filter
- View individual student results
- Results overview with status filtering and CSV export
- Question management (create, edit, delete, bulk import)

## Quick Start (Docker)

```bash
cd d:\apti
docker compose up --build
```

- Student portal: http://localhost:5174
- API docs: http://localhost:8000/docs
- Admin: http://localhost:5174/admin (admin / admin123)

## Local Development

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
# Set environment variables in .env
uvicorn app.main:app --reload --port 8000
```

Required environment variables:
```
DATABASE_URL=postgresql://user:password@localhost:5432/aptitude_db
SECRET_KEY=your-secret-key-change-in-production
CORS_ORIGINS=http://localhost:5174,http://localhost:3000
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Required environment variables:
```
VITE_API_URL=http://localhost:8000
```

## Student Flow

1. Enter Name, Department, Roll Number
2. Read rules page → Start test
3. Answer 30 questions within 30 minutes
4. Anti-cheat violations → Immediate disqualification
5. View results: Score (X/30), Percentage, Status (PASS/FAIL/DISQUALIFIED)

## Anti-Cheating Features

The system automatically disqualifies students for:
- **Tab switching** - Switching tabs or windows during test
- **Screenshot attempts** - Pressing Print Screen key
- **Clipboard abuse** - Pasting large text (>500 chars) or multiple copies
- **Dev tools** - Opening browser developer tools
- **Suspicious patterns** - Multiple copy operations in short time

Disqualification reasons displayed:
- TAB_SWITCH_DETECTED
- SCREENSHOT_DETECTED
- SUSPICIOUS_CLIPBOARD_ACTIVITY
- SUSPICIOUS_COPY_ACTIVITY
- DEV_TOOLS_DETECTED

## API Endpoints

### Public Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/student/login | Student registration/login |
| POST | /api/test/start | Start test for student |
| POST | /api/test/save-answer | Save answer during test |
| POST | /api/test/submit | Submit test |
| GET | /api/result/{roll_number} | Get result by roll number |

### Admin Endpoints (JWT Required)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/admin/login | Admin login |
| GET | /api/results/stats | Dashboard statistics |
| GET | /api/results | List all results |
| GET | /api/results/export | Export results as CSV |
| GET | /api/students | List all students |
| GET | /api/students/{id} | Get student result |
| GET | /api/questions | List questions |
| POST | /api/questions | Create question |
| PUT | /api/questions/{id} | Update question |
| DELETE | /api/questions/{id} | Delete question |
| POST | /api/questions/bulk-import | Bulk import questions |

## Railway Deployment

### Single Container Deployment (Recommended)

The application is configured for single-container deployment on Railway:

1. Create a new Railway project
2. Add **PostgreSQL** plugin → copy `DATABASE_URL`
3. Deploy from repository with existing `Dockerfile` and `railway.toml`
4. Set environment variables in Railway:
   - `DATABASE_URL` (from PostgreSQL plugin)
   - `SECRET_KEY` (generate a secure random string)
   - `CORS_ORIGINS=*` (or specific domains)
   - `ADMIN_USERNAME=admin`
   - `ADMIN_PASSWORD=admin123`
5. Railway will automatically:
   - Build frontend React app
   - Copy to backend static directory
   - Serve both from single container
   - Auto-create database tables on startup
   - Seed initial questions

The admin portal will be available at: `https://your-app.railway.app/admin`

### Troubleshooting Railway Deployment

If admin pages don't load:
1. Check Railway logs for build errors
2. Verify `DATABASE_URL` is correctly set
3. Ensure frontend build completes successfully
4. Check CORS configuration
5. Verify admin credentials are set

## Project Structure

```
apti/
├── backend/
│   ├── app/
│   │   ├── models/        # SQLAlchemy models
│   │   ├── routers/       # API endpoints
│   │   ├── schemas/       # Pydantic schemas
│   │   ├── services/      # Business logic
│   │   ├── utils/         # Utilities (auth, etc.)
│   │   ├── config.py      # Configuration
│   │   ├── database.py    # Database setup
│   │   └── main.py        # FastAPI app
│   ├── alembic/           # Database migrations
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── pages/         # React pages
│   │   ├── components/    # Reusable components
│   │   ├── hooks/         # Custom hooks (anti-cheat)
│   │   ├── api/           # API services
│   │   └── context/       # React context
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
├── Dockerfile            # Multi-stage build for Railway
└── railway.toml
```

## Default Credentials

**Admin Login:**
- Username: `admin`
- Password: `admin123`

⚠️ **Change these in production via environment variables**

## Database Schema

### Students
- id, name, department, roll_number, created_at

### Questions
- id, question, option_a, option_b, option_c, option_d, correct_answer, difficulty, topic

### Answers
- id, student_id, question_id, selected_option

### Results
- id, student_id, score, correct_answers, wrong_answers, percentage, status, disqualification_reason, submitted_at

## License

© 2026 Capgemini Assessment Platform
