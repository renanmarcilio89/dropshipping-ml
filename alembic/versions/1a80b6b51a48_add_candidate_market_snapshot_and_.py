"""add candidate market snapshot and enrichment fields

Revision ID: 1a80b6b51a48
Revises: 6c8eaec31dc1
Create Date: 2026-03-26 18:05:25.560100

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision: str = '1a80b6b51a48'
down_revision: Union[str, Sequence[str], None] = '6c8eaec31dc1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("candidate", sa.Column("last_enriched_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("candidate", sa.Column("enrichment_reason", sa.Text(), nullable=True))

    op.create_table(
        "candidate_market_snapshot",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("candidate_id", sa.Integer(), nullable=False),
        sa.Column("site_id", sa.Text(), nullable=False),
        sa.Column("query_term", sa.Text(), nullable=False),
        sa.Column("predicted_domain_id", sa.Text(), nullable=True),
        sa.Column("predicted_domain_name", sa.Text(), nullable=True),
        sa.Column("predicted_category_id", sa.Text(), nullable=True),
        sa.Column("predicted_category_name", sa.Text(), nullable=True),
        sa.Column("search_total", sa.Integer(), nullable=True),
        sa.Column("sample_size", sa.Integer(), nullable=False),
        sa.Column("unique_seller_count", sa.Integer(), nullable=False),
        sa.Column("price_min", sa.Numeric(12, 2), nullable=True),
        sa.Column("price_max", sa.Numeric(12, 2), nullable=True),
        sa.Column("price_avg", sa.Numeric(12, 2), nullable=True),
        sa.Column("price_median", sa.Numeric(12, 2), nullable=True),
        sa.Column("free_shipping_ratio", sa.Numeric(8, 4), nullable=True),
        sa.Column("catalog_listing_ratio", sa.Numeric(8, 4), nullable=True),
        sa.Column("official_store_ratio", sa.Numeric(8, 4), nullable=True),
        sa.Column("new_condition_ratio", sa.Numeric(8, 4), nullable=True),
        sa.Column("category_total_items", sa.Integer(), nullable=True),
        sa.Column("captured_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["candidate_id"], ["candidate.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_candidate_market_snapshot_candidate_id",
        "candidate_market_snapshot",
        ["candidate_id"],
        unique=False,
    )
    op.create_index(
        "ix_candidate_market_snapshot_captured_at",
        "candidate_market_snapshot",
        ["captured_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_candidate_market_snapshot_captured_at", table_name="candidate_market_snapshot")
    op.drop_index("ix_candidate_market_snapshot_candidate_id", table_name="candidate_market_snapshot")
    op.drop_table("candidate_market_snapshot")

    op.drop_column("candidate", "enrichment_reason")
    op.drop_column("candidate", "last_enriched_at")
