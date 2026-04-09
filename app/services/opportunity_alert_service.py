from __future__ import annotations

from typing import Any


class OpportunityAlertService:
    def evaluate(self, item: dict[str, Any]) -> dict | None:
        final_score = item.get("final_score") or 0
        confidence = item.get("prediction_confidence_level")
        listing_allowed = item.get("listing_allowed")

        if (
            final_score < 0.65
            or confidence not in {"high", "medium"}
            or listing_allowed is not True
        ):
            return None

        reasons = []

        if confidence == "high":
            reasons.append("alta confiança de predição")

        if item.get("term_specificity_level") == "high":
            reasons.append("termo com intenção clara")

        if (item.get("category_total_items") or 0) < 5000:
            reasons.append("categoria com baixa saturação")

        if (item.get("required_attributes_count") or 0) <= 3:
            reasons.append("baixa complexidade operacional")

        if (item.get("important_attributes_count") or 0) > 5:
            reasons.append("boa estrutura de atributos")

        return {
            "candidate_id": item["candidate_id"],
            "term": item["term"],
            "final_score": final_score,
            "confidence": confidence,
            "category": item.get("predicted_category_name"),
            "reasons": reasons,
            "action": "avaliar produto para venda imediata",
        }
