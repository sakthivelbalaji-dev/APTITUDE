"""add attempt number and created at to results

Revision ID: 002
Revises: 001
Create Date: 2026-06-04

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "002"
down_revision: Union[str, None] = "001"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add attempt_number column
    op.add_column('results', sa.Column('attempt_number', sa.Integer(), nullable=True, default=1))
    
    # Add created_at column
    op.add_column('results', sa.Column('created_at', sa.DateTime(), nullable=True))
    
    # Update existing records to have attempt_number = 1
    op.execute("UPDATE results SET attempt_number = 1 WHERE attempt_number IS NULL")
    
    # Make attempt_number non-nullable with default
    op.alter_column('results', 'attempt_number', nullable=False, server_default='1')
    
    # Drop the unique constraint on student_id to allow multiple attempts
    op.drop_constraint('uq_results_student_id', 'results', type_='unique')
    
    # Add index on student_id for better query performance
    op.create_index('ix_results_student_id', 'results', ['student_id'])


def downgrade() -> None:
    # Remove index on student_id
    op.drop_index('ix_results_student_id', table_name='results')
    
    # Add back unique constraint on student_id
    op.create_unique_constraint('uq_results_student_id', 'results', ['student_id'])
    
    # Remove attempt_number column
    op.drop_column('results', 'attempt_number')
    
    # Remove created_at column
    op.drop_column('results', 'created_at')
