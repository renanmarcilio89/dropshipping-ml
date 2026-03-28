from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from statistics import median
from typing import Any

from app.clients.mercadolivre_client import MercadoLivreClient
from app.services.search_service import SearchService


@dataclass(frozen=True)
class CandidateEnrichmentResult:
    captured_at: datetime
    predicted_domain_id: str | None
    predicted_domain_name: str | None
    predicted_category_id: str | None
    predicted_category_name: str | None
    search_total: int | None
    sample_size: int
    unique_seller_count: int
    price_min: float | None
    price_max: float | None
    price_avg: float | None
    price_median: float | None
    free_shipping_ratio: float | None
    catalog_listing_ratio: float | None
    official_store_ratio: float | None
    new_condition_ratio: float | None
    category_total_items: int | None
    prediction_payload: list[dict[str, Any]]
    search_payload: dict[str, Any]
    items_payload: list[dict[str, Any]]
    category_payload: dict[str, Any] | None


class CandidateEnrichmentService:
    def __init__(self, client: MercadoLivreClient) -> None:
        self.client = client

    def enrich(
        self,
        *,
        query: str,
        site_id: str,
        search_limit: int = 20,
    ) -> CandidateEnrichmentResult:
        captured_at = datetime.now(timezone.utc)

        prediction_payload = self.client.predict_category(query=query, site_id=site_id, limit=3)
        top_prediction = prediction_payload[0] if prediction_payload else None

        search_payload = self.client.search_items(
            query=query,
            site_id=site_id,
            limit=search_limit,
        )

        results = search_payload.get("results", []) or []
        item_ids = [item["id"] for item in results if "id" in item][:20]

        items_payload = self.client.get_items(item_ids) if item_ids else []

        predicted_category_id = (
            top_prediction.get("category_id") if top_prediction else None
        )
        category_payload = (
            self.client.get_category(predicted_category_id)
            if predicted_category_id
            else None
        )

        item_bodies = [
            entry.get("body", {})
            for entry in items_payload
            if isinstance(entry, dict) and entry.get("body")
        ]

        prices = [
            float(body["price"])
            for body in item_bodies
            if body.get("price") is not None
        ]

        seller_ids = {
            body.get("seller_id")
            for body in item_bodies
            if body.get("seller_id") is not None
        }

        free_shipping_count = sum(
            1
            for body in item_bodies
            if ((body.get("shipping") or {}).get("free_shipping") is True)
        )

        catalog_listing_count = sum(
            1
            for body in item_bodies
            if body.get("catalog_listing") is True
        )

        official_store_count = sum(
            1
            for body in item_bodies
            if body.get("official_store_id") is not None
        )

        new_condition_count = sum(
            1
            for body in item_bodies
            if body.get("condition") == "new"
        )

        sample_size = len(item_bodies)

        return CandidateEnrichmentResult(
            captured_at=captured_at,
            predicted_domain_id=top_prediction.get("domain_id") if top_prediction else None,
            predicted_domain_name=top_prediction.get("domain_name") if top_prediction else None,
            predicted_category_id=predicted_category_id,
            predicted_category_name=top_prediction.get("category_name") if top_prediction else None,
            search_total=search_payload.get("paging", {}).get("total"),
            sample_size=sample_size,
            unique_seller_count=len(seller_ids),
            price_min=min(prices) if prices else None,
            price_max=max(prices) if prices else None,
            price_avg=(sum(prices) / len(prices)) if prices else None,
            price_median=median(prices) if prices else None,
            free_shipping_ratio=(free_shipping_count / sample_size) if sample_size else None,
            catalog_listing_ratio=(catalog_listing_count / sample_size) if sample_size else None,
            official_store_ratio=(official_store_count / sample_size) if sample_size else None,
            new_condition_ratio=(new_condition_count / sample_size) if sample_size else None,
            category_total_items=(
                category_payload.get("total_items_in_this_category")
                if category_payload
                else None
            ),
            prediction_payload=prediction_payload,
            search_payload=search_payload,
            items_payload=items_payload,
            category_payload=category_payload,
        )

    @staticmethod
    def payload_hash(payload: Any) -> str:
        return SearchService.payload_hash(payload)
