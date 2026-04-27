from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '238560d6ccf9'
down_revision: Union[str, Sequence[str], None] = '1a80b6b51a48'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "candidate_market_snapshot",
        sa.Column("prediction_found", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column(
        "candidate_market_snapshot",
        sa.Column("predicted_attributes_count", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column(
        "candidate_market_snapshot",
        sa.Column("predicted_attributes", sa.JSON(), nullable=True),
    )
    op.add_column(
        "candidate_market_snapshot",
        sa.Column("category_path", sa.JSON(), nullable=True),
    )
    op.add_column(
        "candidate_market_snapshot",
        sa.Column("category_path_text", sa.Text(), nullable=True),
    )
    op.add_column(
        "candidate_market_snapshot",
        sa.Column("category_depth", sa.Integer(), nullable=True),
    )
    op.add_column(
        "candidate_market_snapshot",
        sa.Column("catalog_domain", sa.Text(), nullable=True),
    )
    op.add_column(
        "candidate_market_snapshot",
        sa.Column("listing_allowed", sa.Boolean(), nullable=True),
    )
    op.add_column(
        "candidate_market_snapshot",
        sa.Column("buying_modes", sa.JSON(), nullable=True),
    )
    op.add_column(
        "candidate_market_snapshot",
        sa.Column("required_attributes_count", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column(
        "candidate_market_snapshot",
        sa.Column("important_attributes_count", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column(
        "candidate_market_snapshot",
        sa.Column("attribute_types_summary", sa.JSON(), nullable=True),
    )
    op.add_column(
        "candidate_market_snapshot",
        sa.Column("top_relevant_attributes", sa.JSON(), nullable=True),
    )
    op.add_column(
        "candidate_market_snapshot",
        sa.Column("term_token_count", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column(
        "candidate_market_snapshot",
        sa.Column("term_specificity_level", sa.Text(), nullable=False, server_default="low"),
    )
    op.add_column(
        "candidate_market_snapshot",
        sa.Column("prediction_confidence_score", sa.Numeric(8, 4), nullable=True),
    )
    op.add_column(
        "candidate_market_snapshot",
        sa.Column("prediction_confidence_level", sa.Text(), nullable=True),
    )

    op.create_index(
        "ix_candidate_market_snapshot_predicted_category_id",
        "candidate_market_snapshot",
        ["predicted_category_id"],
        unique=False,
    )

    op.drop_column("candidate_market_snapshot", "search_total")
    op.drop_column("candidate_market_snapshot", "sample_size")
    op.drop_column("candidate_market_snapshot", "unique_seller_count")
    op.drop_column("candidate_market_snapshot", "price_min")
    op.drop_column("candidate_market_snapshot", "price_max")
    op.drop_column("candidate_market_snapshot", "price_avg")
    op.drop_column("candidate_market_snapshot", "price_median")
    op.drop_column("candidate_market_snapshot", "free_shipping_ratio")
    op.drop_column("candidate_market_snapshot", "catalog_listing_ratio")
    op.drop_column("candidate_market_snapshot", "official_store_ratio")
    op.drop_column("candidate_market_snapshot", "new_condition_ratio")


def downgrade() -> None:
    op.add_column(
        "candidate_market_snapshot",
        sa.Column("new_condition_ratio", sa.Numeric(8, 4), nullable=True),
    )
    op.add_column(
        "candidate_market_snapshot",
        sa.Column("official_store_ratio", sa.Numeric(8, 4), nullable=True),
    )
    op.add_column(
        "candidate_market_snapshot",
        sa.Column("catalog_listing_ratio", sa.Numeric(8, 4), nullable=True),
    )
    op.add_column(
        "candidate_market_snapshot",
        sa.Column("free_shipping_ratio", sa.Numeric(8, 4), nullable=True),
    )
    op.add_column(
        "candidate_market_snapshot",
        sa.Column("price_median", sa.Numeric(12, 2), nullable=True),
    )
    op.add_column(
        "candidate_market_snapshot",
        sa.Column("price_avg", sa.Numeric(12, 2), nullable=True),
    )
    op.add_column(
        "candidate_market_snapshot",
        sa.Column("price_max", sa.Numeric(12, 2), nullable=True),
    )
    op.add_column(
        "candidate_market_snapshot",
        sa.Column("price_min", sa.Numeric(12, 2), nullable=True),
    )
    op.add_column(
        "candidate_market_snapshot",
        sa.Column("unique_seller_count", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column(
        "candidate_market_snapshot",
        sa.Column("sample_size", sa.Integer(), nullable=False, server_default="0"),
    )
    op.add_column(
        "candidate_market_snapshot",
        sa.Column("search_total", sa.Integer(), nullable=True),
    )

    op.drop_index(
        "ix_candidate_market_snapshot_predicted_category_id",
        table_name="candidate_market_snapshot",
    )

    op.drop_column("candidate_market_snapshot", "prediction_confidence_level")
    op.drop_column("candidate_market_snapshot", "prediction_confidence_score")
    op.drop_column("candidate_market_snapshot", "term_specificity_level")
    op.drop_column("candidate_market_snapshot", "term_token_count")
    op.drop_column("candidate_market_snapshot", "top_relevant_attributes")
    op.drop_column("candidate_market_snapshot", "attribute_types_summary")
    op.drop_column("candidate_market_snapshot", "important_attributes_count")
    op.drop_column("candidate_market_snapshot", "required_attributes_count")
    op.drop_column("candidate_market_snapshot", "buying_modes")
    op.drop_column("candidate_market_snapshot", "listing_allowed")
    op.drop_column("candidate_market_snapshot", "catalog_domain")
    op.drop_column("candidate_market_snapshot", "category_depth")
    op.drop_column("candidate_market_snapshot", "category_path_text")
    op.drop_column("candidate_market_snapshot", "category_path")
    op.drop_column("candidate_market_snapshot", "predicted_attributes")
    op.drop_column("candidate_market_snapshot", "predicted_attributes_count")
    op.drop_column("candidate_market_snapshot", "prediction_found")
