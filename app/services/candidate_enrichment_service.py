from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from app.clients.mercadolivre_client import MercadoLivreClient
from app.services.search_service import SearchService


@dataclass(frozen=True)
class CandidateEnrichmentResult:
    captured_at: datetime
    prediction_found: bool

    predicted_domain_id: str | None
    predicted_domain_name: str | None
    predicted_category_id: str | None
    predicted_category_name: str | None

    predicted_attributes_count: int
    predicted_attributes: list[dict[str, Any]]

    category_path: list[dict[str, Any]] | None
    category_path_text: str | None
    category_depth: int | None
    category_total_items: int | None

    catalog_domain: str | None
    listing_allowed: bool | None
    buying_modes: list[str] | None

    required_attributes_count: int
    important_attributes_count: int
    attribute_types_summary: dict[str, int]
    top_relevant_attributes: list[dict[str, Any]]

    term_token_count: int
    term_specificity_level: str
    prediction_confidence_score: float
    prediction_confidence_level: str

    prediction_payload: list[dict[str, Any]]
    category_payload: dict[str, Any] | None
    category_attributes_payload: list[dict[str, Any]]


class CandidateEnrichmentService:
    def __init__(self, client: MercadoLivreClient) -> None:
        self.client = client

    def enrich(
        self,
        *,
        query: str,
        site_id: str,
    ) -> CandidateEnrichmentResult:
        captured_at = datetime.now(timezone.utc)

        normalized_query = (query or "").strip()
        prediction_payload = self.client.predict_category(
            query=normalized_query,
            site_id=site_id,
            limit=3,
        )

        top_prediction = prediction_payload[0] if prediction_payload else None
        predicted_category_id = (
            top_prediction.get("category_id") if top_prediction else None
        )

        category_payload = (
            self.client.get_category(predicted_category_id)
            if predicted_category_id
            else None
        )

        category_attributes_payload = (
            self.client.get_category_attributes(predicted_category_id)
            if predicted_category_id
            else []
        )

        predicted_attributes = []
        if top_prediction:
            predicted_attributes = top_prediction.get("attributes") or []

        category_path = None
        category_path_text = None
        category_depth = None
        category_total_items = None
        catalog_domain = None
        listing_allowed = None
        buying_modes = None

        if category_payload:
            category_path = category_payload.get("path_from_root") or []
            category_path_text = self._build_category_path_text(category_path)
            category_depth = len(category_path) if category_path else 0
            category_total_items = category_payload.get("total_items_in_this_category")

            settings = category_payload.get("settings") or {}
            catalog_domain = settings.get("catalog_domain")
            listing_allowed = settings.get("listing_allowed")
            buying_modes = settings.get("buying_modes") or []

        required_attributes_count = self._count_required_attributes(
            category_attributes_payload
        )
        important_attributes = self._extract_important_attributes(
            category_attributes_payload
        )
        attribute_types_summary = self._summarize_attribute_types(
            category_attributes_payload
        )

        term_token_count = self._term_token_count(normalized_query)
        predicted_attributes_count = len(predicted_attributes)

        term_specificity_level = self._term_specificity_level(
            token_count=term_token_count,
            category_depth=category_depth or 0,
            predicted_attributes_count=predicted_attributes_count,
        )

        prediction_confidence_score = self._prediction_confidence_score(
            prediction_found=top_prediction is not None,
            category_depth=category_depth or 0,
            predicted_attributes_count=predicted_attributes_count,
            required_attributes_count=required_attributes_count,
        )
        prediction_confidence_level = self._prediction_confidence_level(
            prediction_confidence_score
        )

        return CandidateEnrichmentResult(
            captured_at=captured_at,
            prediction_found=top_prediction is not None,
            predicted_domain_id=top_prediction.get("domain_id") if top_prediction else None,
            predicted_domain_name=top_prediction.get("domain_name") if top_prediction else None,
            predicted_category_id=predicted_category_id,
            predicted_category_name=top_prediction.get("category_name") if top_prediction else None,
            predicted_attributes_count=predicted_attributes_count,
            predicted_attributes=predicted_attributes,
            category_path=category_path,
            category_path_text=category_path_text,
            category_depth=category_depth,
            category_total_items=category_total_items,
            catalog_domain=catalog_domain,
            listing_allowed=listing_allowed,
            buying_modes=buying_modes,
            required_attributes_count=required_attributes_count,
            important_attributes_count=len(important_attributes),
            attribute_types_summary=attribute_types_summary,
            top_relevant_attributes=important_attributes[:15],
            term_token_count=term_token_count,
            term_specificity_level=term_specificity_level,
            prediction_confidence_score=prediction_confidence_score,
            prediction_confidence_level=prediction_confidence_level,
            prediction_payload=prediction_payload,
            category_payload=category_payload,
            category_attributes_payload=category_attributes_payload,
        )

    @staticmethod
    def payload_hash(payload: Any) -> str:
        return SearchService.payload_hash(payload)

    @staticmethod
    def _build_category_path_text(path: list[dict[str, Any]]) -> str | None:
        if not path:
            return None
        names = [node.get("name") for node in path if node.get("name")]
        return " > ".join(names) if names else None

    @staticmethod
    def _count_required_attributes(attributes_payload: list[dict[str, Any]]) -> int:
        count = 0
        for attr in attributes_payload:
            tags = attr.get("tags") or {}
            if tags.get("required") is True:
                count += 1
        return count

    @staticmethod
    def _extract_important_attributes(
        attributes_payload: list[dict[str, Any]],
    ) -> list[dict[str, Any]]:
        important: list[dict[str, Any]] = []

        for attr in attributes_payload:
            tags = attr.get("tags") or {}
            relevance = int(attr.get("relevance") or 0)

            if tags.get("hidden") is True:
                continue

            if tags.get("required") is True or relevance >= 1:
                important.append(
                    {
                        "id": attr.get("id"),
                        "name": attr.get("name"),
                        "value_type": attr.get("value_type"),
                        "relevance": relevance,
                        "required": tags.get("required", False),
                        "attribute_group_id": attr.get("attribute_group_id"),
                        "attribute_group_name": attr.get("attribute_group_name"),
                    }
                )

        important.sort(
            key=lambda item: (
                0 if item["required"] else 1,
                -(item["relevance"] or 0),
                item["name"] or "",
            )
        )
        return important

    @staticmethod
    def _summarize_attribute_types(
        attributes_payload: list[dict[str, Any]],
    ) -> dict[str, int]:
        summary: dict[str, int] = {}

        for attr in attributes_payload:
            value_type = attr.get("value_type")
            if not value_type:
                continue
            summary[value_type] = summary.get(value_type, 0) + 1

        return summary

    @staticmethod
    def _term_token_count(query: str) -> int:
        return len([token for token in query.split() if token.strip()])

    @staticmethod
    def _term_specificity_level(
        *,
        token_count: int,
        category_depth: int,
        predicted_attributes_count: int,
    ) -> str:
        if category_depth >= 4 or predicted_attributes_count >= 3 or token_count >= 4:
            return "high"

        if category_depth >= 3 or predicted_attributes_count >= 2 or token_count >= 2:
            return "medium"

        return "low"

    @staticmethod
    def _prediction_confidence_score(
        *,
        prediction_found: bool,
        category_depth: int,
        predicted_attributes_count: int,
        required_attributes_count: int,
    ) -> float:
        if not prediction_found:
            return 0.0

        score = 0.35

        if category_depth >= 2:
            score += 0.15
        if category_depth >= 3:
            score += 0.10
        if category_depth >= 4:
            score += 0.05

        score += min(predicted_attributes_count * 0.08, 0.20)
        score += min(required_attributes_count * 0.03, 0.15)

        return round(min(score, 0.95), 4)

    @staticmethod
    def _prediction_confidence_level(score: float) -> str:
        if score >= 0.80:
            return "high"
        if score >= 0.55:
            return "medium"
        if score > 0:
            return "low"
        return "none"
