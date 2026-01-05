"""initial migration

Revision ID: 001
Revises: 
Create Date: 2026-01-05

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'fingerprints',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('hash', sa.String(length=32), nullable=False),
        sa.Column('risk_score', sa.Float(), nullable=True),
        sa.Column('is_bot', sa.Boolean(), nullable=True),
        sa.Column('first_seen', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.Column('last_seen', sa.DateTime(timezone=True), nullable=True),
        sa.Column('visit_count', sa.Integer(), nullable=True),
        sa.Column('canvas', sa.String(), nullable=True),
        sa.Column('webgl', sa.String(), nullable=True),
        sa.Column('audio', sa.String(), nullable=True),
        sa.Column('fonts', sa.String(), nullable=True),
        sa.Column('hardware', sa.String(), nullable=True),
        sa.Column('screen', sa.String(), nullable=True),
        sa.Column('browser', sa.String(), nullable=True),
        sa.Column('timezone', sa.String(), nullable=True),
        sa.Column('plugins', sa.String(), nullable=True),
        sa.Column('touch', sa.String(), nullable=True),
        sa.Column('battery', sa.String(), nullable=True),
        sa.Column('network', sa.String(), nullable=True),
        sa.Column('media', sa.String(), nullable=True),
        sa.Column('color_depth', sa.String(), nullable=True),
        sa.Column('do_not_track', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_fingerprints_hash'), 'fingerprints', ['hash'], unique=True)
    op.create_index(op.f('ix_fingerprints_id'), 'fingerprints', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_fingerprints_id'), table_name='fingerprints')
    op.drop_index(op.f('ix_fingerprints_hash'), table_name='fingerprints')
    op.drop_table('fingerprints')
