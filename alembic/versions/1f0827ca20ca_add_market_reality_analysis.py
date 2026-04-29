"""add market reality analysis

Revision ID: 1f0827ca20ca
Revises: 4d9f2c1a8b77
Create Date: 2026-04-29 06:04:55.994030

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision: str = '1f0827ca20ca'
down_revision: Union[str, Sequence[str], None] = '4d9f2c1a8b77'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "market_reality_analysis",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("candidate_id", sa.Integer(), nullable=False),
        sa.Column("sale_price", sa.Numeric(12, 2), nullable=False),
        sa.Column("supplier_cost", sa.Numeric(12, 2), nullable=False),
        sa.Column("shipping_cost", sa.Numeric(12, 2), nullable=False),
        sa.Column("marketplace_fee_rate", sa.Numeric(8, 4), nullable=False),
        sa.Column("ads_cost_rate", sa.Numeric(8, 4), nullable=False),
        sa.Column("marketplace_fee", sa.Numeric(12, 2), nullable=False),
        sa.Column("ads_cost", sa.Numeric(12, 2), nullable=False),
        sa.Column("total_cost", sa.Numeric(12, 2), nullable=False),
        sa.Column("estimated_profit", sa.Numeric(12, 2), nullable=False),
        sa.Column("estimated_margin", sa.Numeric(10, 4), nullable=False),
        sa.Column("break_even_price", sa.Numeric(12, 2), nullable=False),
        sa.Column("viability_level", sa.Text(), nullable=False),
        sa.Column("recommendation", sa.Text(), nullable=False),
        sa.Column("analysis_version", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["candidate_id"], ["candidate.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_market_reality_analysis_candidate_id",
        "market_reality_analysis",
        ["candidate_id"],
        unique=False,
    )
    op.create_index(
        "ix_market_reality_analysis_created_at",
        "market_reality_analysis",
        ["created_at"],
        unique=False,
    )
    op.create_index(
        "ix_market_reality_analysis_viability_level",
        "market_reality_analysis",
        ["viability_level"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        "ix_market_reality_analysis_viability_level",
        table_name="market_reality_analysis",
    )
    op.drop_index(
        "ix_market_reality_analysis_created_at",
        table_name="market_reality_analysis",
    )
    op.drop_index(
        "ix_market_reality_analysis_candidate_id",
        table_name="market_reality_analysis",
    )
    op.drop_table("market_reality_analysis")
