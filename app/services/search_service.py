from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

from app.clients.mercadolivre_client import MercadoLivreClient
from app.schemas.common import SearchItemRecord


class SearchService:
    def __init__(self, client: MercadoLivreClient) -> None:
        self.client = client

    @staticmethod
    def payload_hash(payload: Any) -> str:
        return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()

    def fetch_trends(self, site_id: str) -> tuple[list[str], str, datetime]:
        payload = self.client.get_trends(site_id=site_id)
        captured_at = datetime.now(timezone.utc)
        terms = [item['keyword'] for item in payload if 'keyword' in item]
        return terms, self.payload_hash(payload), captured_at

    def search_marketplace(self, query: str, site_id: str, offset: int = 0) -> tuple[list[SearchItemRecord], str, datetime]:
        payload = self.client.search_items(query=query, site_id=site_id, offset=offset)
        captured_at = datetime.now(timezone.utc)
        results = payload.get('results', [])
        items = []
        for entry in results:
            shipping = entry.get('shipping') or {}
            seller = entry.get('seller') or {}
            items.append(
                SearchItemRecord(
                    item_id=entry['id'],
                    title=entry.get('title'),
                    seller_id=seller.get('id'),
                    category_id=entry.get('category_id'),
                    price=entry.get('price'),
                    listing_type_id=entry.get('listing_type_id'),
                    catalog_listing=entry.get('catalog_listing'),
                    free_shipping=shipping.get('free_shipping'),
                    logistic_type=shipping.get('logistic_type'),
                )
            )
        return items, self.payload_hash(payload), captured_at
