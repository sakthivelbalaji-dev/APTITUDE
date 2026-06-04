"""remove password add resume to students

Revision ID: 004
Revises: 003
Create Date: 2026-06-04

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "004"
down_revision: Union[str, None] = "003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add resume_path column as nullable first
    op.add_column('students', sa.Column('resume_path', sa.Text(), nullable=True))
    
    # Remove password column
    op.drop_column('students', 'password')


def downgrade() -> None:
    # Add password column back as nullable first
    op.add_column('students', sa.Column('password', sa.String(255), nullable=True))
    
    # Set a default password for existing students
    import hashlib
    default_password = hashlib.sha256("changeme123".encode()).hexdigest()
    op.execute(f"UPDATE students SET password = '{default_password}' WHERE password IS NULL")
    
    # Make password non-nullable
    op.alter_column('students', 'password', nullable=False)
    
    # Remove resume_path column
    op.drop_column('students', 'resume_path')
