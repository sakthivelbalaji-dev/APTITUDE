# Capgemini Aptitude Assessment Portal

Mobile-first aptitude test platform for college students with admin management, anti-cheating, and PostgreSQL backend.

## Tech Stack

- **Frontend:** React (Vite) + Tailwind CSS + Axios
- **Backend:** FastAPI + SQLAlchemy + Alembic
- **Database:** PostgreSQL
- **Auth:** JWT (Admin only)
- **Deploy:** Docker + Railway

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
# Start PostgreSQL and set DATABASE_URL in .env
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

## Student Flow

1. Enter Name, Department, Roll Number
2. Rules page → Start test
3. 30 questions (15 easy + 15 medium), 30 minutes
4. Anti-cheat: tab switch / blur → DISQUALIFIED
5. Results: PASS (≥50%), FAIL, or DISQUALIFIED

## API Endpoints

| Method | Endpoint | Auth |
|--------|----------|------|
| POST | /student/login | Public |
| POST | /test/start | Public |
| POST | /test/save-answer | Public |
| POST | /test/submit | Public |
| GET | /result/{roll_number} | Public |
| POST | /admin/login | Public |
| GET/POST/PUT/DELETE | /questions | Admin JWT |
| GET | /students, /students/{id} | Admin JWT |
| GET | /results, /results/stats, /results/export | Admin JWT |

## Railway Deployment

1. Create a new Railway project
2. Add **PostgreSQL** plugin → copy `DATABASE_URL`
3. Deploy **backend** service from `backend/` folder:
   - `DATABASE_URL`, `SECRET_KEY`, `CORS_ORIGINS` (frontend URL)
   - `ADMIN_USERNAME`, `ADMIN_PASSWORD`
4. Deploy **frontend** service from `frontend/`:
   - `VITE_API_URL` = backend public URL (set at build time)
5. Run migrations: `alembic upgrade head` (or tables auto-create on startup)

## Project Structure

```
apti/
├── backend/app/          # FastAPI application
├── frontend/src/         # React application
├── docker-compose.yml
└── railway.toml
```

© 2026 Capgemini Assessment Platform
