import os
import sys
from sqlalchemy import inspect, text

from app.database import engine

def ensure_password_column():
    """Ensure the password column exists in the students table"""
    inspector = inspect(engine)
    
    # Get existing columns
    columns = [col['name'] for col in inspector.get_columns('students')]
    print(f"Existing columns in students table: {columns}")
    
    if 'password' not in columns:
        print("Password column missing. Adding it...")
        with engine.connect() as conn:
            # Add password column as nullable first
            conn.execute(text("ALTER TABLE students ADD COLUMN password VARCHAR(255)"))
            conn.commit()
            
            # Set a default password for existing students
            import hashlib
            default_password = hashlib.sha256("changeme123".encode()).hexdigest()
            conn.execute(text(f"UPDATE students SET password = '{default_password}' WHERE password IS NULL"))
            conn.commit()
            
            # Make password non-nullable (PostgreSQL requires this to be done separately)
            conn.execute(text("ALTER TABLE students ALTER COLUMN password SET NOT NULL"))
            conn.commit()
            
        print("Password column added successfully")
    else:
        print("Password column already exists")

if __name__ == "__main__":
    try:
        ensure_password_column()
        print("Database schema check completed successfully")
    except Exception as e:
        print(f"Error ensuring schema: {e}")
        import traceback
        print(traceback.format_exc())
        sys.exit(1)
