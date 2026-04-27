from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class OpportunityScoringResult:
    captured_at: datetime
    demand_score: float
    competition_score: float
    quality_score: float
    ops_risk_score: float
    final_score: float
    score_version: str


class OpportunityScoringService:
    SCORE_VERSION = "v1_structural_prediction_quality"

    def score(self, snapshot: Any) -> OpportunityScoringResult:
        captured_at = datetime.now(timezone.utc)

        demand_score = self._demand_score(snapshot)
        competition_score = self._competition_score(snapshot)
        quality_score = self._quality_score(snapshot)
        ops_risk_score = self._ops_risk_score(snapshot)

        final_score = round(
            (demand_score * 0.30)
            + (competition_score * 0.25)
            + (quality_score * 0.25)
            + (ops_risk_score * 0.20),
            4,
        )

        return OpportunityScoringResult(
            captured_at=captured_at,
            demand_score=demand_score,
            competition_score=competition_score,
            quality_score=quality_score,
            ops_risk_score=ops_risk_score,
            final_score=final_score,
            score_version=self.SCORE_VERSION,
        )

    def _demand_score(self, snapshot: Any) -> float:
        confidence = float(snapshot.prediction_confidence_score or 0.0)
        specificity = self._specificity_to_score(snapshot.term_specificity_level or "low")
        depth_score = min((snapshot.category_depth or 0) / 5.0, 1.0)
        prediction_quality_multiplier = self._prediction_quality_multiplier(snapshot)

        score = (
            (confidence * 0.5)
            + (specificity * 0.3)
            + (depth_score * 0.2)
        )

        score *= prediction_quality_multiplier

        return round(max(0.0, min(score, 1.0)), 4)

    def _competition_score(self, snapshot: Any) -> float:
        total_items = snapshot.category_total_items
        depth = snapshot.category_depth or 0

        breadth_penalty = self._category_total_items_penalty(total_items)
        depth_bonus = min(depth / 5.0, 1.0) * 0.25
        prediction_quality_penalty = self._prediction_quality_competition_penalty(snapshot)

        score = (1.0 - breadth_penalty) + depth_bonus - prediction_quality_penalty
        score = max(0.0, min(1.0, score))

        return round(score, 4)

    def _quality_score(self, snapshot: Any) -> float:
        confidence = float(snapshot.prediction_confidence_score or 0.0)

        predicted_attributes_count = snapshot.predicted_attributes_count or 0
        important_attributes_count = snapshot.important_attributes_count or 0

        predicted_attr_score = min(predicted_attributes_count / 5.0, 1.0)
        important_attr_score = min(important_attributes_count / 12.0, 1.0)
        prediction_quality_multiplier = self._prediction_quality_multiplier(snapshot)

        score = (
            (confidence * 0.55)
            + (predicted_attr_score * 0.20)
            + (important_attr_score * 0.25)
        )

        score *= prediction_quality_multiplier

        return round(max(0.0, min(score, 1.0)), 4)

    def _ops_risk_score(self, snapshot: Any) -> float:
        score = 1.0

        if snapshot.listing_allowed is False:
            score -= 0.60

        required_attributes_count = snapshot.required_attributes_count or 0
        score -= min(required_attributes_count * 0.04, 0.30)

        buying_modes = snapshot.buying_modes or []
        if not buying_modes:
            score -= 0.10

        score -= self._prediction_quality_ops_penalty(snapshot)

        return round(max(0.0, min(score, 1.0)), 4)

    @staticmethod
    def _specificity_to_score(level: str) -> float:
        mapping = {
            "high": 1.0,
            "medium": 0.65,
            "low": 0.35,
            "none": 0.0,
        }
        return mapping.get(level, 0.35)

    @staticmethod
    def _category_total_items_penalty(total_items: int | None) -> float:
        if total_items is None:
            return 0.35
        if total_items <= 500:
            return 0.10
        if total_items <= 2_000:
            return 0.20
        if total_items <= 10_000:
            return 0.40
        if total_items <= 50_000:
            return 0.60
        return 0.80

    @staticmethod
    def _prediction_quality(snapshot: Any) -> dict[str, Any]:
        summary = snapshot.attribute_types_summary or {}
        quality = summary.get("_prediction_quality")

        if isinstance(quality, dict):
            return quality

        return {
            "level": "unknown",
            "confidence_penalty": 0.0,
            "reasons": [],
            "alternatives_count": 0,
            "distinct_categories_count": 0,
            "distinct_domains_count": 0,
        }

    @classmethod
    def _prediction_quality_multiplier(cls, snapshot: Any) -> float:
        quality = cls._prediction_quality(snapshot)
        level = quality.get("level")
        penalty = float(quality.get("confidence_penalty") or 0.0)

        if level == "low":
            return max(0.55, 1.0 - penalty)
        if level == "medium":
            return max(0.75, 1.0 - penalty)
        if level == "high":
            return 1.0

        return max(0.85, 1.0 - penalty)

    @classmethod
    def _prediction_quality_competition_penalty(cls, snapshot: Any) -> float:
        quality = cls._prediction_quality(snapshot)
        level = quality.get("level")
        penalty = float(quality.get("confidence_penalty") or 0.0)

        if level == "low":
            return min(0.20, penalty * 0.50)
        if level == "medium":
            return min(0.10, penalty * 0.35)

        return 0.0

    @classmethod
    def _prediction_quality_ops_penalty(cls, snapshot: Any) -> float:
        quality = cls._prediction_quality(snapshot)
        level = quality.get("level")
        penalty = float(quality.get("confidence_penalty") or 0.0)

        if level == "low":
            return min(0.20, penalty * 0.60)
        if level == "medium":
            return min(0.10, penalty * 0.40)

        return 0.0
