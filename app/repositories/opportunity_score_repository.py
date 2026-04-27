from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.market import OpportunityScore


class OpportunityScoreRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(
        self,
        *,
        candidate_id: int,
        demand_score: float,
        competition_score: float,
        quality_score: float,
        ops_risk_score: float,
        final_score: float,
        score_version: str,
        captured_at: datetime,
    ) -> OpportunityScore:
        row = OpportunityScore(
            candidate_id=candidate_id,
            demand_score=demand_score,
            competition_score=competition_score,
            quality_score=quality_score,
            ops_risk_score=ops_risk_score,
            final_score=final_score,
            score_version=score_version,
            captured_at=captured_at,
        )
        self.session.add(row)
        self.session.flush()
        self.session.refresh(row)
        return row

    def get_latest_by_candidate_id(self, candidate_id: int) -> OpportunityScore | None:
        stmt = (
            select(OpportunityScore)
            .where(OpportunityScore.candidate_id == candidate_id)
            .order_by(OpportunityScore.captured_at.desc(), OpportunityScore.id.desc())
        )
        return self.session.execute(stmt).scalars().first()
