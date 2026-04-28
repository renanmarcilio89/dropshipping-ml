from __future__ import annotations

from typing import Any


class CommercialOpportunityService:
    def build_output(self, opportunities: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [self.analyze(opportunity) for opportunity in opportunities]

    def analyze(self, opportunity: dict[str, Any]) -> dict[str, Any]:
        commercial_score = self._commercial_score(opportunity)
        decision = self._decision(opportunity, commercial_score)
        risk_level = self._risk_level(opportunity)
        monetization_fit = self._monetization_fit(opportunity, commercial_score, risk_level)

        return {
            "candidate_id": opportunity["candidate_id"],
            "term": opportunity["term"],
            "final_score": opportunity["final_score"],
            "commercial_score": commercial_score,
            "commercial_decision": decision,
            "monetization_fit": monetization_fit,
            "risk_level": risk_level,
            "recommended_action": self._recommended_action(decision),
            "reasons": self._reasons(opportunity, decision, commercial_score, risk_level),
            "missing_data": self._missing_data(opportunity, decision),
        }

    def _commercial_score(self, opportunity: dict[str, Any]) -> float:
        demand = self._float(opportunity.get("demand_score"))
        competition = self._float(opportunity.get("competition_score"))
        quality = self._float(opportunity.get("quality_score"))
        ops = self._float(opportunity.get("ops_risk_score"))
        prediction = self._prediction_reliability(opportunity)
        price = self._price_signal(opportunity)

        score = (
            demand * 0.28
            + competition * 0.20
            + quality * 0.15
            + ops * 0.10
            + prediction * 0.12
            + price * 0.15
        )

        return round(max(0.0, min(score, 1.0)), 4)

    def _decision(self, opportunity: dict[str, Any], score: float) -> str:
        if opportunity.get("listing_allowed") is False:
            return "avoid"

        if opportunity.get("prediction_quality_level") == "low":
            return "avoid"

        risk_level = self._risk_level(opportunity)

        if risk_level == "high":
            if score >= 0.60:
                return "affiliate_candidate"
            if score >= 0.50:
                return "research_needed"
            return "avoid"

        if score >= 0.72 and risk_level == "low":
            return "dropshipping_candidate"

        if score >= 0.60:
            return "affiliate_candidate"

        if score >= 0.50:
            return "research_needed"

        return "avoid"

    def _risk_level(self, opportunity: dict[str, Any]) -> str:
        required = int(opportunity.get("required_attributes_count") or 0)
        items = opportunity.get("category_total_items")

        risk = 0

        if required >= 10:
            risk += 2
        elif required >= 6:
            risk += 1

        if items is not None:
            if items > 50000:
                risk += 2
            elif items > 10000:
                risk += 1

        if risk >= 3:
            return "high"
        if risk >= 1:
            return "medium"
        return "low"

    def _monetization_fit(self, opportunity, score, risk):
        if score >= 0.72 and risk == "low":
            return "high"
        if score >= 0.58:
            return "medium"
        return "low"

    def _recommended_action(self, decision: str) -> str:
        if decision == "dropshipping_candidate":
            return "Validate supplier cost, shipping, marketplace fees, delivery time, and minimum viable margin before creating an offer."

        if decision == "affiliate_candidate":
            return "Validate demand with affiliate links or content before taking supplier, shipping, or inventory exposure."

        if decision == "research_needed":
            return "Collect real offer prices, supplier options, fees, shipping constraints, and competitor data before choosing a monetization path."

        return "Do not prioritize this opportunity until the structural risks or prediction quality improve."

    def _reasons(self, opportunity, decision, score, risk):
        reasons = []

        if score > 0.7:
            reasons.append("High commercial score.")
        elif score > 0.55:
            reasons.append("Moderate commercial score.")

        if opportunity.get("prediction_quality_level") in ["high", "medium"]:
            reasons.append("Good prediction quality.")

        if risk == "low":
            reasons.append("Low operational risk.")
        elif risk == "high":
            reasons.append("High operational complexity.")

        return reasons

    def _missing_data(self, opportunity, decision):
        return [
            "Supplier cost",
            "Marketplace fees",
            "Shipping cost",
            "Competition pricing",
        ]

    def _prediction_reliability(self, opportunity):
        confidence = self._float(opportunity.get("prediction_confidence_score"))
        penalty = self._float(opportunity.get("prediction_quality_penalty"))
        return max(0.0, min(confidence - penalty, 1.0))
    
    def _price_signal(self, opportunity):
        avg_price = opportunity.get("avg_price")

        if avg_price is None:
            return 0.5

        if avg_price >= 100:
            return 0.9
        if avg_price >= 50:
            return 0.7
        if avg_price >= 20:
            return 0.5

        return 0.3

    @staticmethod
    def _float(value):
        return float(value or 0.0)
