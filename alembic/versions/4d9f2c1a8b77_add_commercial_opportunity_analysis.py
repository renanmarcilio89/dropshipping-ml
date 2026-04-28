from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "4d9f2c1a8b77"
down_revision: Union[str, Sequence[str], None] = "ef5796c86bb5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "commercial_opportunity_analysis",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("candidate_id", sa.Integer(), nullable=False),
        sa.Column("commercial_score", sa.Numeric(10, 4), nullable=False),
        sa.Column("commercial_decision", sa.Text(), nullable=False),
        sa.Column("monetization_fit", sa.Text(), nullable=False),
        sa.Column("risk_level", sa.Text(), nullable=False),
        sa.Column("recommended_action", sa.Text(), nullable=False),
        sa.Column("reason_payload", sa.JSON(), nullable=False),
        sa.Column("missing_data_payload", sa.JSON(), nullable=False),
        sa.Column("source_payload", sa.JSON(), nullable=False),
        sa.Column("analysis_version", sa.Text(), nullable=False),
        sa.Column(
            "captured_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["candidate_id"], ["candidate.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_commercial_opportunity_analysis_candidate_id",
        "commercial_opportunity_analysis",
        ["candidate_id"],
        unique=False,
    )
    op.create_index(
        "ix_commercial_opportunity_analysis_captured_at",
        "commercial_opportunity_analysis",
        ["captured_at"],
        unique=False,
    )
    op.create_index(
        "ix_commercial_opportunity_analysis_decision",
        "commercial_opportunity_analysis",
        ["commercial_decision"],
        unique=False,
    )
    op.create_index(
        "ix_commercial_opportunity_analysis_risk_level",
        "commercial_opportunity_analysis",
        ["risk_level"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_commercial_opportunity_analysis_risk_level",
        table_name="commercial_opportunity_analysis",
    )
    op.drop_index(
        "ix_commercial_opportunity_analysis_decision",
        table_name="commercial_opportunity_analysis",
    )
    op.drop_index(
        "ix_commercial_opportunity_analysis_captured_at",
        table_name="commercial_opportunity_analysis",
    )
    op.drop_index(
        "ix_commercial_opportunity_analysis_candidate_id",
        table_name="commercial_opportunity_analysis",
    )
    op.drop_table("commercial_opportunity_analysis")
