"""add password to students

Revision ID: 003
Revises: 002
Create Date: 2026-06-04

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "003"
down_revision: Union[str, None] = "002"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add password column as nullable first
    op.add_column('students', sa.Column('password', sa.String(255), nullable=True))
    
    # Set a default password for existing students (they will need to reset it)
    # Using a temporary default password "changeme123"
    from app.utils.auth import get_password_hash
    default_password = get_password_hash("changeme123")
    op.execute(f"UPDATE students SET password = '{default_password}' WHERE password IS NULL")
    
    # Make password non-nullable
    op.alter_column('students', 'password', nullable=False)


def downgrade() -> None:
    # Remove password column
    op.drop_column('students', 'password')
