from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class TrendRecord(BaseModel):
    keyword: str = Field(alias='keyword')
    url: str | None = None


class SearchItemRecord(BaseModel):
    item_id: str
    title: str | None = None
    seller_id: int | None = None
    category_id: str | None = None
    price: float | None = None
    listing_type_id: str | None = None
    catalog_listing: bool | None = None
    free_shipping: bool | None = None
    logistic_type: str | None = None


class ItemAttributeRecord(BaseModel):
    attribute_id: str
    attribute_name: str | None = None
    value_id: str | None = None
    value_name: str | None = None
    value_struct: dict[str, Any] | None = None


class ItemRecord(BaseModel):
    item_id: str
    site_id: str
    seller_id: int | None = None
    title: str | None = None
    category_id: str | None = None
    domain_id: str | None = None
    price: float | None = None
    currency_id: str | None = None
    available_quantity_ref: int | None = None
    condition: str | None = None
    listing_type_id: str | None = None
    catalog_listing: bool | None = None
    permalink: str | None = None
    thumbnail: str | None = None
    official_store_id: int | None = None
    accepts_mercadopago: bool | None = None
    buying_mode: str | None = None
    status: str | None = None
    shipping_mode: str | None = None
    shipping_tags: list[str] | None = None
    seller_address_city: str | None = None
    seller_address_state: str | None = None
    attributes: list[ItemAttributeRecord] = []


class OpportunityBreakdown(BaseModel):
    entity_type: str
    entity_id: str
    captured_at: datetime
    demand_score: float
    traction_score: float
    competition_score: float
    quality_score: float
    ops_risk_score: float
    final_score: float
    score_version: str
