from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

from app.clients.mercadolivre_client import MercadoLivreClient
from app.schemas.common import ItemAttributeRecord, ItemRecord


class ItemService:
    def __init__(self, client: MercadoLivreClient) -> None:
        self.client = client

    @staticmethod
    def payload_hash(payload: Any) -> str:
        return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()

    def enrich_items(self, item_ids: list[str], site_id: str) -> tuple[list[ItemRecord], str, datetime]:
        payload = self.client.get_items(item_ids)
        captured_at = datetime.now(timezone.utc)
        items: list[ItemRecord] = []

        for wrapper in payload:
            body = wrapper.get('body') or {}
            attributes = [
                ItemAttributeRecord(
                    attribute_id=attr.get('id', ''),
                    attribute_name=attr.get('name'),
                    value_id=attr.get('value_id'),
                    value_name=attr.get('value_name'),
                    value_struct=attr.get('value_struct'),
                )
                for attr in body.get('attributes', [])
                if attr.get('id')
            ]
            shipping = body.get('shipping') or {}
            seller_address = body.get('seller_address') or {}
            city = (seller_address.get('city') or {}).get('name')
            state = (seller_address.get('state') or {}).get('name')

            items.append(
                ItemRecord(
                    item_id=body['id'],
                    site_id=site_id,
                    seller_id=body.get('seller_id'),
                    title=body.get('title'),
                    category_id=body.get('category_id'),
                    domain_id=body.get('domain_id'),
                    price=body.get('price'),
                    currency_id=body.get('currency_id'),
                    available_quantity_ref=body.get('available_quantity'),
                    condition=body.get('condition'),
                    listing_type_id=body.get('listing_type_id'),
                    catalog_listing=body.get('catalog_listing'),
                    permalink=body.get('permalink'),
                    thumbnail=body.get('thumbnail'),
                    official_store_id=body.get('official_store_id'),
                    accepts_mercadopago=body.get('accepts_mercadopago'),
                    buying_mode=body.get('buying_mode'),
                    status=body.get('status'),
                    shipping_mode=shipping.get('mode'),
                    shipping_tags=shipping.get('tags') or [],
                    seller_address_city=city,
                    seller_address_state=state,
                    attributes=attributes,
                )
            )
        return items, self.payload_hash(payload), captured_at
