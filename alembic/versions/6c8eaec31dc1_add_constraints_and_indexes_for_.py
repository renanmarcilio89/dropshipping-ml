"""add constraints and indexes for pipeline foundations

Revision ID: 6c8eaec31dc1
Revises: d4fb6f3df9fd
Create Date: 2026-03-26 16:36:31.635835

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision: str = '6c8eaec31dc1'
down_revision: Union[str, Sequence[str], None] = 'd4fb6f3df9fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_candidate_normalized_term",
        "candidate",
        ["normalized_term"],
    )
    op.create_index(
        "ix_candidate_status",
        "candidate",
        ["status"],
        unique=False,
    )
    op.create_index(
        "ix_candidate_qualification_status",
        "candidate",
        ["qualification_status"],
        unique=False,
    )

    op.create_index(
        "ix_trend_snapshot_captured_at",
        "trend_snapshot",
        ["captured_at"],
        unique=False,
    )
    op.create_index(
        "ix_trend_snapshot_site_id_captured_at",
        "trend_snapshot",
        ["site_id", "captured_at"],
        unique=False,
    )

    op.create_unique_constraint(
        "uq_api_payload_payload_hash",
        "api_payload",
        ["payload_hash"],
    )
    op.create_index(
        "ix_api_payload_captured_at",
        "api_payload",
        ["captured_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_api_payload_captured_at", table_name="api_payload")
    op.drop_constraint("uq_api_payload_payload_hash", "api_payload", type_="unique")

    op.drop_index("ix_trend_snapshot_site_id_captured_at", table_name="trend_snapshot")
    op.drop_index("ix_trend_snapshot_captured_at", table_name="trend_snapshot")

    op.drop_index("ix_candidate_qualification_status", table_name="candidate")
    op.drop_index("ix_candidate_status", table_name="candidate")
    op.drop_constraint("uq_candidate_normalized_term", "candidate", type_="unique")
