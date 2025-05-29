"""add table oznameni

Revision ID: 20240525_add_oznameni
Revises: 22a4bfb9d189
Create Date: 2025-05-25 19:20:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '20240525_add_oznameni'
down_revision = '22a4bfb9d189'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'oznameni',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True, nullable=False),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('vytvoreno', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('cilovy_uzivatel_id', postgresql.UUID(as_uuid=True), nullable=True),  # např. notifikace pro uživatele
    )

def downgrade():
    op.drop_table('oznameni')
