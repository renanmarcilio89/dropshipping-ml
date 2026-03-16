from datetime import datetime

from sqlalchemy import JSON, BigInteger, Boolean, DateTime, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class CategoryDim(Base):
    __tablename__ = 'category_dim'
    __table_args__ = {'schema': 'ml_core'}

    category_id: Mapped[str] = mapped_column(String, primary_key=True)
    site_id: Mapped[str] = mapped_column(String, nullable=False)
    category_name: Mapped[str] = mapped_column(String, nullable=False)
    path_from_root: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    is_leaf: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    date_first_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    date_last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class TrendSnapshot(Base):
    __tablename__ = 'trend_snapshot'
    __table_args__ = {'schema': 'ml_core'}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    site_id: Mapped[str] = mapped_column(String, nullable=False)
    term: Mapped[str] = mapped_column(String, nullable=False)
    rank_position: Mapped[int | None] = mapped_column(Integer, nullable=True)
    source: Mapped[str] = mapped_column(String, default='trends')
    window_type: Mapped[str] = mapped_column(String, default='weekly')
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class SearchSnapshot(Base):
    __tablename__ = 'search_snapshot'
    __table_args__ = {'schema': 'ml_core'}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    site_id: Mapped[str] = mapped_column(String, nullable=False)
    query: Mapped[str] = mapped_column(String, nullable=False)
    offset_value: Mapped[int] = mapped_column(Integer, default=0)
    result_position: Mapped[int] = mapped_column(Integer, nullable=False)
    item_id: Mapped[str] = mapped_column(String, nullable=False)
    seller_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    category_id: Mapped[str | None] = mapped_column(String, nullable=True)
    price: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True)
    listing_type_id: Mapped[str | None] = mapped_column(String, nullable=True)
    catalog_listing_flag: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    free_shipping_flag: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    shipping_logistic_type: Mapped[str | None] = mapped_column(String, nullable=True)
    raw_payload_hash: Mapped[str | None] = mapped_column(String, nullable=True)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ItemSnapshot(Base):
    __tablename__ = 'item_snapshot'
    __table_args__ = (
        UniqueConstraint('item_id', 'captured_at', name='uq_item_snapshot_item_time'),
        {'schema': 'ml_core'},
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    item_id: Mapped[str] = mapped_column(String, nullable=False)
    site_id: Mapped[str] = mapped_column(String, nullable=False)
    seller_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    title: Mapped[str | None] = mapped_column(Text, nullable=True)
    category_id: Mapped[str | None] = mapped_column(String, nullable=True)
    domain_id: Mapped[str | None] = mapped_column(String, nullable=True)
    price: Mapped[float | None] = mapped_column(Numeric(18, 2), nullable=True)
    currency_id: Mapped[str | None] = mapped_column(String, nullable=True)
    available_quantity_ref: Mapped[int | None] = mapped_column(Integer, nullable=True)
    condition: Mapped[str | None] = mapped_column(String, nullable=True)
    listing_type_id: Mapped[str | None] = mapped_column(String, nullable=True)
    catalog_listing_flag: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    permalink: Mapped[str | None] = mapped_column(Text, nullable=True)
    thumbnail: Mapped[str | None] = mapped_column(Text, nullable=True)
    official_store_id: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    accepts_mercadopago: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    buying_mode: Mapped[str | None] = mapped_column(String, nullable=True)
    status: Mapped[str | None] = mapped_column(String, nullable=True)
    shipping_mode: Mapped[str | None] = mapped_column(String, nullable=True)
    shipping_tags: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    seller_address_city: Mapped[str | None] = mapped_column(String, nullable=True)
    seller_address_state: Mapped[str | None] = mapped_column(String, nullable=True)
    attributes_hash: Mapped[str | None] = mapped_column(String, nullable=True)
    raw_payload_hash: Mapped[str | None] = mapped_column(String, nullable=True)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)


class ItemAttributeSnapshot(Base):
    __tablename__ = 'item_attribute_snapshot'
    __table_args__ = {'schema': 'ml_core'}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    item_id: Mapped[str] = mapped_column(String, nullable=False)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    attribute_id: Mapped[str] = mapped_column(String, nullable=False)
    attribute_name: Mapped[str | None] = mapped_column(String, nullable=True)
    value_id: Mapped[str | None] = mapped_column(String, nullable=True)
    value_name: Mapped[str | None] = mapped_column(String, nullable=True)
    value_struct: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    source: Mapped[str] = mapped_column(String, default='items')
