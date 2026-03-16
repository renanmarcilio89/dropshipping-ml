from datetime import datetime

from sqlalchemy.orm import Session

from app.models.core import ItemAttributeSnapshot, ItemSnapshot, SearchSnapshot, TrendSnapshot
from app.schemas.common import ItemRecord, SearchItemRecord


class SearchRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def save_trends(self, site_id: str, terms: list[str], captured_at: datetime) -> int:
        rows = [
            TrendSnapshot(site_id=site_id, term=term, rank_position=idx + 1, captured_at=captured_at)
            for idx, term in enumerate(terms)
        ]
        self.db.add_all(rows)
        self.db.commit()
        return len(rows)

    def save_search_results(
        self,
        site_id: str,
        query: str,
        items: list[SearchItemRecord],
        captured_at: datetime,
        offset: int = 0,
        raw_payload_hash: str | None = None,
    ) -> int:
        rows = []
        for idx, item in enumerate(items, start=1 + offset):
            rows.append(
                SearchSnapshot(
                    site_id=site_id,
                    query=query,
                    offset_value=offset,
                    result_position=idx,
                    item_id=item.item_id,
                    seller_id=item.seller_id,
                    category_id=item.category_id,
                    price=item.price,
                    listing_type_id=item.listing_type_id,
                    catalog_listing_flag=item.catalog_listing,
                    free_shipping_flag=item.free_shipping,
                    shipping_logistic_type=item.logistic_type,
                    raw_payload_hash=raw_payload_hash,
                    captured_at=captured_at,
                )
            )
        self.db.add_all(rows)
        self.db.commit()
        return len(rows)

    def save_item_snapshot(self, item: ItemRecord, captured_at: datetime, raw_payload_hash: str | None) -> None:
        item_row = ItemSnapshot(
            item_id=item.item_id,
            site_id=item.site_id,
            seller_id=item.seller_id,
            title=item.title,
            category_id=item.category_id,
            domain_id=item.domain_id,
            price=item.price,
            currency_id=item.currency_id,
            available_quantity_ref=item.available_quantity_ref,
            condition=item.condition,
            listing_type_id=item.listing_type_id,
            catalog_listing_flag=item.catalog_listing,
            permalink=item.permalink,
            thumbnail=item.thumbnail,
            official_store_id=item.official_store_id,
            accepts_mercadopago=item.accepts_mercadopago,
            buying_mode=item.buying_mode,
            status=item.status,
            shipping_mode=item.shipping_mode,
            shipping_tags={'tags': item.shipping_tags or []},
            seller_address_city=item.seller_address_city,
            seller_address_state=item.seller_address_state,
            raw_payload_hash=raw_payload_hash,
            captured_at=captured_at,
        )
        self.db.add(item_row)
        self.db.flush()

        attrs = [
            ItemAttributeSnapshot(
                item_id=item.item_id,
                captured_at=captured_at,
                attribute_id=attr.attribute_id,
                attribute_name=attr.attribute_name,
                value_id=attr.value_id,
                value_name=attr.value_name,
                value_struct=attr.value_struct,
            )
            for attr in item.attributes
        ]
        self.db.add_all(attrs)
        self.db.commit()
