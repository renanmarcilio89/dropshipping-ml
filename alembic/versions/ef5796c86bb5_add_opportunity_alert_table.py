from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'ef5796c86bb5'
down_revision: Union[str, Sequence[str], None] = '238560d6ccf9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "opportunity_alert",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("candidate_id", sa.Integer(), sa.ForeignKey("candidate.id"), nullable=False),
        sa.Column("alert_hash", sa.Text(), nullable=False),
        sa.Column("alert_version", sa.Text(), nullable=False),
        sa.Column("score_version", sa.Text(), nullable=True),
        sa.Column("final_score", sa.Numeric(10, 4), nullable=False),
        sa.Column("confidence_level", sa.Text(), nullable=True),
        sa.Column("category_id", sa.Text(), nullable=True),
        sa.Column("category_name", sa.Text(), nullable=True),
        sa.Column("action", sa.Text(), nullable=False),
        sa.Column("reason_payload", sa.JSON(), nullable=False),
        sa.Column("status", sa.Text(), nullable=False, server_default="open"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.UniqueConstraint("alert_hash", name="uq_opportunity_alert_alert_hash"),
    )

    op.create_index("ix_opportunity_alert_candidate_id", "opportunity_alert", ["candidate_id"], unique=False)
    op.create_index("ix_opportunity_alert_status", "opportunity_alert", ["status"], unique=False)
    op.create_index("ix_opportunity_alert_created_at", "opportunity_alert", ["created_at"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_opportunity_alert_created_at", table_name="opportunity_alert")
    op.drop_index("ix_opportunity_alert_status", table_name="opportunity_alert")
    op.drop_index("ix_opportunity_alert_candidate_id", table_name="opportunity_alert")
    op.drop_table("opportunity_alert")
