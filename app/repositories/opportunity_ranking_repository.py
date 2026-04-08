from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.market import Candidate, CandidateMarketSnapshot, OpportunityScore


class OpportunityRankingRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_top_opportunities(self, limit: int = 20) -> list:
        latest_score_subquery = (
            select(
                OpportunityScore.candidate_id.label("candidate_id"),
                func.max(OpportunityScore.captured_at).label("max_scored_at"),
            )
            .group_by(OpportunityScore.candidate_id)
            .subquery()
        )

        latest_snapshot_subquery = (
            select(
                CandidateMarketSnapshot.candidate_id.label("candidate_id"),
                func.max(CandidateMarketSnapshot.captured_at).label("max_snapshot_at"),
            )
            .group_by(CandidateMarketSnapshot.candidate_id)
            .subquery()
        )

        stmt = (
            select(
                Candidate.id.label("candidate_id"),
                Candidate.normalized_term,
                Candidate.candidate_type,
                CandidateMarketSnapshot.predicted_category_id,
                CandidateMarketSnapshot.predicted_category_name,
                CandidateMarketSnapshot.category_path_text,
                CandidateMarketSnapshot.category_total_items,
                CandidateMarketSnapshot.prediction_confidence_score,
                CandidateMarketSnapshot.prediction_confidence_level,
                CandidateMarketSnapshot.term_specificity_level,
                CandidateMarketSnapshot.listing_allowed,
                CandidateMarketSnapshot.required_attributes_count,
                CandidateMarketSnapshot.important_attributes_count,
                OpportunityScore.demand_score,
                OpportunityScore.competition_score,
                OpportunityScore.quality_score,
                OpportunityScore.ops_risk_score,
                OpportunityScore.final_score,
                OpportunityScore.score_version,
                OpportunityScore.captured_at.label("scored_at"),
            )
            .join(
                latest_score_subquery,
                latest_score_subquery.c.candidate_id == Candidate.id,
            )
            .join(
                OpportunityScore,
                (OpportunityScore.candidate_id == latest_score_subquery.c.candidate_id)
                & (OpportunityScore.captured_at == latest_score_subquery.c.max_scored_at),
            )
            .join(
                latest_snapshot_subquery,
                latest_snapshot_subquery.c.candidate_id == Candidate.id,
            )
            .join(
                CandidateMarketSnapshot,
                (CandidateMarketSnapshot.candidate_id == latest_snapshot_subquery.c.candidate_id)
                & (CandidateMarketSnapshot.captured_at == latest_snapshot_subquery.c.max_snapshot_at),
            )
            .order_by(
                OpportunityScore.final_score.desc(),
                OpportunityScore.demand_score.desc(),
                Candidate.id.asc(),
            )
            .limit(limit)
        )

        return list(self.session.execute(stmt).all())
