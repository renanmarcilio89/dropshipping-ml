from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

from app.clients.mercadolivre_client import MercadoLivreClient


class SearchService:
    def __init__(self, client: MercadoLivreClient) -> None:
        self.client = client

    @staticmethod
    def payload_hash(payload: Any) -> str:
        return hashlib.sha256(
            json.dumps(payload, sort_keys=True, default=str).encode()
        ).hexdigest()

    def fetch_trends(
        self,
        site_id: str,
    ) -> tuple[list[str], list[dict[str, Any]], str, datetime]:
        payload = self.client.get_trends(site_id=site_id)
        captured_at = datetime.now(timezone.utc)
        terms = [item["keyword"] for item in payload if "keyword" in item]
        return terms, payload, self.payload_hash(payload), captured_at
