"""initial schema

Revision ID: 0001_initial
Revises:
Create Date: 2026-03-16 00:00:00.000000
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = '0001_initial'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute('CREATE SCHEMA IF NOT EXISTS ml_core')
    op.execute('CREATE SCHEMA IF NOT EXISTS ml_analytics')

    op.create_table(
        'category_dim',
        sa.Column('category_id', sa.String(), nullable=False),
        sa.Column('site_id', sa.String(), nullable=False),
        sa.Column('category_name', sa.String(), nullable=False),
        sa.Column('path_from_root', sa.JSON(), nullable=True),
        sa.Column('is_leaf', sa.Boolean(), nullable=True),
        sa.Column('date_first_seen', sa.DateTime(timezone=True), nullable=False),
        sa.Column('date_last_seen', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('category_id'),
        schema='ml_core',
    )

    op.create_table(
        'trend_snapshot',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('site_id', sa.String(), nullable=False),
        sa.Column('term', sa.String(), nullable=False),
        sa.Column('rank_position', sa.Integer(), nullable=True),
        sa.Column('source', sa.String(), nullable=False),
        sa.Column('window_type', sa.String(), nullable=False),
        sa.Column('captured_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema='ml_core',
    )

    op.create_table(
        'search_snapshot',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('site_id', sa.String(), nullable=False),
        sa.Column('query', sa.String(), nullable=False),
        sa.Column('offset_value', sa.Integer(), nullable=False),
        sa.Column('result_position', sa.Integer(), nullable=False),
        sa.Column('item_id', sa.String(), nullable=False),
        sa.Column('seller_id', sa.BigInteger(), nullable=True),
        sa.Column('category_id', sa.String(), nullable=True),
        sa.Column('price', sa.Numeric(18, 2), nullable=True),
        sa.Column('listing_type_id', sa.String(), nullable=True),
        sa.Column('catalog_listing_flag', sa.Boolean(), nullable=True),
        sa.Column('free_shipping_flag', sa.Boolean(), nullable=True),
        sa.Column('shipping_logistic_type', sa.String(), nullable=True),
        sa.Column('raw_payload_hash', sa.String(), nullable=True),
        sa.Column('captured_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema='ml_core',
    )

    op.create_table(
        'item_snapshot',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('item_id', sa.String(), nullable=False),
        sa.Column('site_id', sa.String(), nullable=False),
        sa.Column('seller_id', sa.BigInteger(), nullable=True),
        sa.Column('title', sa.Text(), nullable=True),
        sa.Column('category_id', sa.String(), nullable=True),
        sa.Column('domain_id', sa.String(), nullable=True),
        sa.Column('price', sa.Numeric(18, 2), nullable=True),
        sa.Column('currency_id', sa.String(), nullable=True),
        sa.Column('available_quantity_ref', sa.Integer(), nullable=True),
        sa.Column('condition', sa.String(), nullable=True),
        sa.Column('listing_type_id', sa.String(), nullable=True),
        sa.Column('catalog_listing_flag', sa.Boolean(), nullable=True),
        sa.Column('permalink', sa.Text(), nullable=True),
        sa.Column('thumbnail', sa.Text(), nullable=True),
        sa.Column('official_store_id', sa.BigInteger(), nullable=True),
        sa.Column('accepts_mercadopago', sa.Boolean(), nullable=True),
        sa.Column('buying_mode', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('shipping_mode', sa.String(), nullable=True),
        sa.Column('shipping_tags', sa.JSON(), nullable=True),
        sa.Column('seller_address_city', sa.String(), nullable=True),
        sa.Column('seller_address_state', sa.String(), nullable=True),
        sa.Column('attributes_hash', sa.String(), nullable=True),
        sa.Column('raw_payload_hash', sa.String(), nullable=True),
        sa.Column('captured_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('item_id', 'captured_at', name='uq_item_snapshot_item_time'),
        schema='ml_core',
    )

    op.create_table(
        'item_attribute_snapshot',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('item_id', sa.String(), nullable=False),
        sa.Column('captured_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('attribute_id', sa.String(), nullable=False),
        sa.Column('attribute_name', sa.String(), nullable=True),
        sa.Column('value_id', sa.String(), nullable=True),
        sa.Column('value_name', sa.String(), nullable=True),
        sa.Column('value_struct', sa.JSON(), nullable=True),
        sa.Column('source', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema='ml_core',
    )

    op.create_table(
        'item_feature_fact',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('item_id', sa.String(), nullable=False),
        sa.Column('captured_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('demand_score', sa.Numeric(8, 4), nullable=False),
        sa.Column('traction_score', sa.Numeric(8, 4), nullable=False),
        sa.Column('competition_score', sa.Numeric(8, 4), nullable=False),
        sa.Column('quality_score', sa.Numeric(8, 4), nullable=False),
        sa.Column('ops_risk_score', sa.Numeric(8, 4), nullable=False),
        sa.Column('query_presence_24h', sa.Integer(), nullable=True),
        sa.Column('query_presence_7d', sa.Integer(), nullable=True),
        sa.Column('avg_search_position_24h', sa.Numeric(8, 2), nullable=True),
        sa.Column('avg_search_position_7d', sa.Numeric(8, 2), nullable=True),
        sa.Column('trend_hits_7d', sa.Integer(), nullable=True),
        sa.Column('bestseller_hits_7d', sa.Integer(), nullable=True),
        sa.Column('competitor_cluster_size', sa.Integer(), nullable=True),
        sa.Column('latest_rating_average', sa.Numeric(5, 2), nullable=True),
        sa.Column('score_version', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema='ml_analytics',
    )

    op.create_table(
        'opportunity_score',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('entity_type', sa.String(), nullable=False),
        sa.Column('entity_id', sa.String(), nullable=False),
        sa.Column('captured_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('final_score', sa.Numeric(8, 4), nullable=False),
        sa.Column('demand_score', sa.Numeric(8, 4), nullable=False),
        sa.Column('traction_score', sa.Numeric(8, 4), nullable=False),
        sa.Column('competition_score', sa.Numeric(8, 4), nullable=False),
        sa.Column('quality_score', sa.Numeric(8, 4), nullable=False),
        sa.Column('ops_risk_score', sa.Numeric(8, 4), nullable=False),
        sa.Column('score_version', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema='ml_analytics',
    )

    op.create_table(
        'alert_event',
        sa.Column('alert_id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('alert_type', sa.String(), nullable=False),
        sa.Column('severity', sa.String(), nullable=False),
        sa.Column('entity_type', sa.String(), nullable=False),
        sa.Column('entity_id', sa.String(), nullable=False),
        sa.Column('title', sa.Text(), nullable=False),
        sa.Column('payload_json', sa.JSON(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.PrimaryKeyConstraint('alert_id'),
        schema='ml_analytics',
    )


def downgrade() -> None:
    op.drop_table('alert_event', schema='ml_analytics')
    op.drop_table('opportunity_score', schema='ml_analytics')
    op.drop_table('item_feature_fact', schema='ml_analytics')
    op.drop_table('item_attribute_snapshot', schema='ml_core')
    op.drop_table('item_snapshot', schema='ml_core')
    op.drop_table('search_snapshot', schema='ml_core')
    op.drop_table('trend_snapshot', schema='ml_core')
    op.drop_table('category_dim', schema='ml_core')
