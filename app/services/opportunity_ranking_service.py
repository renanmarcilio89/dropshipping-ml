from __future__ import annotations

from typing import Any


class OpportunityRankingService:
    def build_output(self, rows: list[Any]) -> list[dict]:
        output: list[dict] = []

        for row in rows:
            output.append(
                {
                    "candidate_id": row.candidate_id,
                    "term": row.normalized_term,
                    "candidate_type": row.candidate_type,
                    "predicted_category_id": row.predicted_category_id,
                    "predicted_category_name": row.predicted_category_name,
                    "category_path_text": row.category_path_text,
                    "category_total_items": row.category_total_items,
                    "prediction_confidence_score": self._to_float(row.prediction_confidence_score),
                    "prediction_confidence_level": row.prediction_confidence_level,
                    "term_specificity_level": row.term_specificity_level,
                    "listing_allowed": row.listing_allowed,
                    "required_attributes_count": row.required_attributes_count,
                    "important_attributes_count": row.important_attributes_count,
                    "demand_score": self._to_float(row.demand_score),
                    "competition_score": self._to_float(row.competition_score),
                    "quality_score": self._to_float(row.quality_score),
                    "ops_risk_score": self._to_float(row.ops_risk_score),
                    "final_score": self._to_float(row.final_score),
                    "score_version": row.score_version,
                    "scored_at": row.scored_at.isoformat() if row.scored_at else None,
                }
            )

        return output

    @staticmethod
    def normalize_confidence_level(value: str | None) -> str | None:
        if value is None:
            return None

        normalized = value.strip().lower()
        if normalized in {"high", "medium", "low", "none"}:
            return normalized

        raise ValueError(
            "confidence_level inválido. Use: high, medium, low ou none."
        )

    @staticmethod
    def _to_float(value: Any) -> float | None:
        if value is None:
            return None
        return float(value)
