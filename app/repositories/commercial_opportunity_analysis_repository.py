from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from app.models.market import CommercialOpportunityAnalysis


class CommercialOpportunityAnalysisRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_many(
        self,
        analyses: list[dict[str, Any]],
        *,
        analysis_version: str,
    ) -> list[CommercialOpportunityAnalysis]:
        records = [
            CommercialOpportunityAnalysis(
                candidate_id=analysis["candidate_id"],
                commercial_score=analysis["commercial_score"],
                commercial_decision=analysis["commercial_decision"],
                monetization_fit=analysis["monetization_fit"],
                risk_level=analysis["risk_level"],
                recommended_action=analysis["recommended_action"],
                reason_payload=analysis["reasons"],
                missing_data_payload=analysis["missing_data"],
                source_payload=analysis.get("source", {}),
                analysis_version=analysis_version,
            )
            for analysis in analyses
        ]

        self.session.add_all(records)
        return records
