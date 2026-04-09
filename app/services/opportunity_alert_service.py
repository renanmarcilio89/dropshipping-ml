from __future__ import annotations

import hashlib
import json
from typing import Any


class OpportunityAlertService:
    ALERT_VERSION = "v1_structural_alerts"

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

        reasons: list[str] = []

        if confidence == "high":
            reasons.append("alta confiança de predição")

        if item.get("term_specificity_level") == "high":
            reasons.append("termo com intenção clara")

        category_total_items = item.get("category_total_items")
        if category_total_items is not None and category_total_items < 5000:
            reasons.append("categoria com baixa saturação")

        if (item.get("required_attributes_count") or 0) <= 3:
            reasons.append("baixa complexidade operacional")

        if (item.get("important_attributes_count") or 0) > 5:
            reasons.append("boa estrutura de atributos")

        if not reasons:
            reasons.append("combinação favorável de sinais estruturais")

        payload = {
            "candidate_id": item["candidate_id"],
            "term": item["term"],
            "category": item.get("predicted_category_name"),
            "predicted_category_id": item.get("predicted_category_id"),
            "final_score": final_score,
            "confidence": confidence,
            "score_version": item.get("score_version"),
            "alert_version": self.ALERT_VERSION,
            "reasons": reasons,
            "action": "avaliar produto para venda imediata",
        }

        payload["alert_hash"] = self.build_alert_hash(payload)
        return payload

    @staticmethod
    def build_alert_hash(payload: dict[str, Any]) -> str:
        stable_payload = {
            "candidate_id": payload.get("candidate_id"),
            "term": payload.get("term"),
            "predicted_category_id": payload.get("predicted_category_id"),
            "final_score": round(float(payload.get("final_score") or 0), 4),
            "confidence": payload.get("confidence"),
            "score_version": payload.get("score_version"),
            "alert_version": payload.get("alert_version"),
            "reasons": payload.get("reasons") or [],
            "action": payload.get("action"),
        }
        raw = json.dumps(stable_payload, ensure_ascii=False, sort_keys=True)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()
