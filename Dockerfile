# Build frontend
FROM node:20-alpine AS frontend-build

WORKDIR /app/frontend

COPY frontend/package.json frontend/package-lock.json* ./
RUN npm install

COPY frontend/ .
# Build with empty API URL for same-domain deployment
ENV VITE_API_URL=""
RUN npm run build

# Build backend with frontend static files
FROM python:3.12-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

# Copy frontend build to backend static directory
COPY --from=frontend-build /app/frontend/dist ./static

EXPOSE 8000

# Run migrations, seed database, and start the app
CMD ["sh", "-c", "alembic upgrade head && python -c 'from app.seed import seed_database; seed_database()' && uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
