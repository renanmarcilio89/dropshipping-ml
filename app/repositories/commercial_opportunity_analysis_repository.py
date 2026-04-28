from __future__ import annotations

from typing import Any

from sqlalchemy import select
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

    def list_latest(
        self,
        *,
        limit: int = 20,
        commercial_decision: str | None = None,
        risk_level: str | None = None,
        min_commercial_score: float | None = None,
    ) -> list[CommercialOpportunityAnalysis]:
        stmt = select(CommercialOpportunityAnalysis)

        if commercial_decision is not None:
            stmt = stmt.where(
                CommercialOpportunityAnalysis.commercial_decision == commercial_decision
            )

        if risk_level is not None:
            stmt = stmt.where(CommercialOpportunityAnalysis.risk_level == risk_level)

        if min_commercial_score is not None:
            stmt = stmt.where(
                CommercialOpportunityAnalysis.commercial_score >= min_commercial_score
            )

        stmt = stmt.order_by(
            CommercialOpportunityAnalysis.captured_at.desc(),
            CommercialOpportunityAnalysis.commercial_score.desc(),
            CommercialOpportunityAnalysis.id.desc(),
        ).limit(limit)

        return list(self.session.scalars(stmt).all())
