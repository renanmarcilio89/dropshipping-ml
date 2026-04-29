from __future__ import annotations

from typing import Any


class InvestmentPriorityService:
    def build_output(self, rows: list[Any]) -> list[dict]:
        return [self._build_item(row) for row in rows]

    def _build_item(self, row: Any) -> dict:
        estimated_margin = self._float(row.estimated_margin)
        investment_priority = self._investment_priority(row)
        priority_score = self._priority_score(row)

        return {
            "candidate_id": row.candidate_id,
            "term": row.term,
            "final_score": self._float(row.final_score),
            "commercial_score": self._float(row.commercial_score),
            "commercial_decision": row.commercial_decision,
            "monetization_fit": row.monetization_fit,
            "risk_level": row.risk_level,
            "sale_price": self._float(row.sale_price),
            "supplier_cost": self._float(row.supplier_cost),
            "shipping_cost": self._float(row.shipping_cost),
            "total_cost": self._float(row.total_cost),
            "estimated_profit": self._float(row.estimated_profit),
            "estimated_margin": estimated_margin,
            "estimated_margin_percent": round(estimated_margin * 100, 2),
            "break_even_price": self._float(row.break_even_price),
            "viability_level": row.viability_level,
            "priority_score": priority_score,
            "investment_priority": investment_priority,
            "recommended_action": self._recommended_action(row, investment_priority),
            "commercial_recommended_action": row.commercial_recommended_action,
            "market_reality_recommendation": row.market_reality_recommendation,
            "market_reality_created_at": row.market_reality_created_at.isoformat()
            if row.market_reality_created_at
            else None,
        }

    def _priority_score(self, row: Any) -> float:
        final_score = self._float(row.final_score)
        commercial_score = self._float(row.commercial_score)
        estimated_margin = self._float(row.estimated_margin)
        estimated_profit = self._float(row.estimated_profit)

        normalized_profit = min(max(estimated_profit / 100.0, 0.0), 1.0)
        risk_multiplier = self._risk_multiplier(row.risk_level)
        viability_multiplier = self._viability_multiplier(row.viability_level)

        score = (
            final_score * 0.25
            + commercial_score * 0.35
            + min(max(estimated_margin, 0.0), 1.0) * 0.25
            + normalized_profit * 0.15
        )

        score *= risk_multiplier
        score *= viability_multiplier

        return round(max(0.0, min(score, 1.0)), 4)

    def _investment_priority(self, row: Any) -> str:
        priority_score = self._priority_score(row)

        if row.viability_level == "unprofitable":
            return "avoid"

        if row.risk_level == "high":
            if priority_score >= 0.55:
                return "controlled_validation"
            return "avoid"

        if priority_score >= 0.72:
            return "high_priority"

        if priority_score >= 0.55:
            return "controlled_validation"

        if priority_score >= 0.40:
            return "watchlist"

        return "avoid"

    @staticmethod
    def _recommended_action(row: Any, investment_priority: str) -> str:
        actions = {
            "high_priority": "Prioritize validation with supplier, pricing, demand test, and operating constraints.",
            "controlled_validation": "Run a controlled validation before committing capital or operational exposure.",
            "watchlist": "Keep monitoring and improve margin, demand evidence, or operational conditions before acting.",
            "avoid": "Do not prioritize this opportunity under the current market reality scenario.",
        }
        return actions[investment_priority]

    @staticmethod
    def _risk_multiplier(risk_level: str | None) -> float:
        mapping = {
            "low": 1.0,
            "medium": 0.85,
            "high": 0.65,
        }
        return mapping.get(risk_level, 0.75)

    @staticmethod
    def _viability_multiplier(viability_level: str | None) -> float:
        mapping = {
            "strong": 1.0,
            "viable": 0.9,
            "thin": 0.75,
            "weak": 0.55,
            "unprofitable": 0.0,
        }
        return mapping.get(viability_level, 0.7)

    @staticmethod
    def _float(value: Any) -> float:
        if value is None:
            return 0.0
        return float(value)
