from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '2a5303ff9856'
down_revision: Union[str, Sequence[str], None] = '4c11a24fad27'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'api_payload',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('source_name', sa.Text(), nullable=False),
        sa.Column('site_id', sa.Text(), nullable=True),
        sa.Column('endpoint', sa.Text(), nullable=False),
        sa.Column('request_params', sa.JSON(), nullable=True),
        sa.Column('payload', sa.JSON(), nullable=False),
        sa.Column('payload_hash', sa.Text(), nullable=False),
        sa.Column('captured_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_api_payload_payload_hash', 'api_payload', ['payload_hash'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_api_payload_payload_hash', table_name='api_payload')
    op.drop_table('api_payload')
