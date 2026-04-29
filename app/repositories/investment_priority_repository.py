from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.market import (
    Candidate,
    CommercialOpportunityAnalysis,
    MarketRealityAnalysis,
    OpportunityScore,
)


class InvestmentPriorityRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_priorities(
        self,
        *,
        limit: int = 20,
        min_final_score: float | None = None,
        min_commercial_score: float | None = None,
        min_estimated_margin: float | None = None,
        commercial_decision: str | None = None,
        viability_level: str | None = None,
    ) -> list:
        latest_score_subquery = (
            select(
                OpportunityScore.candidate_id.label("candidate_id"),
                func.max(OpportunityScore.captured_at).label("max_scored_at"),
            )
            .group_by(OpportunityScore.candidate_id)
            .subquery()
        )

        latest_commercial_subquery = (
            select(
                CommercialOpportunityAnalysis.candidate_id.label("candidate_id"),
                func.max(CommercialOpportunityAnalysis.captured_at).label(
                    "max_commercial_at"
                ),
            )
            .group_by(CommercialOpportunityAnalysis.candidate_id)
            .subquery()
        )

        latest_market_reality_subquery = (
            select(
                MarketRealityAnalysis.candidate_id.label("candidate_id"),
                func.max(MarketRealityAnalysis.created_at).label(
                    "max_market_reality_at"
                ),
            )
            .group_by(MarketRealityAnalysis.candidate_id)
            .subquery()
        )

        stmt = (
            select(
                Candidate.id.label("candidate_id"),
                Candidate.normalized_term.label("term"),
                OpportunityScore.final_score,
                OpportunityScore.demand_score,
                OpportunityScore.competition_score,
                OpportunityScore.quality_score,
                OpportunityScore.ops_risk_score,
                CommercialOpportunityAnalysis.commercial_score,
                CommercialOpportunityAnalysis.commercial_decision,
                CommercialOpportunityAnalysis.monetization_fit,
                CommercialOpportunityAnalysis.risk_level,
                CommercialOpportunityAnalysis.recommended_action.label(
                    "commercial_recommended_action"
                ),
                MarketRealityAnalysis.sale_price,
                MarketRealityAnalysis.supplier_cost,
                MarketRealityAnalysis.shipping_cost,
                MarketRealityAnalysis.total_cost,
                MarketRealityAnalysis.estimated_profit,
                MarketRealityAnalysis.estimated_margin,
                MarketRealityAnalysis.break_even_price,
                MarketRealityAnalysis.viability_level,
                MarketRealityAnalysis.recommendation.label(
                    "market_reality_recommendation"
                ),
                MarketRealityAnalysis.created_at.label("market_reality_created_at"),
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
                latest_commercial_subquery,
                latest_commercial_subquery.c.candidate_id == Candidate.id,
            )
            .join(
                CommercialOpportunityAnalysis,
                (
                    CommercialOpportunityAnalysis.candidate_id
                    == latest_commercial_subquery.c.candidate_id
                )
                & (
                    CommercialOpportunityAnalysis.captured_at
                    == latest_commercial_subquery.c.max_commercial_at
                ),
            )
            .join(
                latest_market_reality_subquery,
                latest_market_reality_subquery.c.candidate_id == Candidate.id,
            )
            .join(
                MarketRealityAnalysis,
                (
                    MarketRealityAnalysis.candidate_id
                    == latest_market_reality_subquery.c.candidate_id
                )
                & (
                    MarketRealityAnalysis.created_at
                    == latest_market_reality_subquery.c.max_market_reality_at
                ),
            )
        )

        if min_final_score is not None:
            stmt = stmt.where(OpportunityScore.final_score >= min_final_score)

        if min_commercial_score is not None:
            stmt = stmt.where(
                CommercialOpportunityAnalysis.commercial_score >= min_commercial_score
            )

        if min_estimated_margin is not None:
            stmt = stmt.where(
                MarketRealityAnalysis.estimated_margin >= min_estimated_margin
            )

        if commercial_decision is not None:
            stmt = stmt.where(
                CommercialOpportunityAnalysis.commercial_decision
                == commercial_decision
            )

        if viability_level is not None:
            stmt = stmt.where(MarketRealityAnalysis.viability_level == viability_level)

        stmt = stmt.order_by(
            CommercialOpportunityAnalysis.commercial_score.desc(),
            MarketRealityAnalysis.estimated_margin.desc(),
            OpportunityScore.final_score.desc(),
            MarketRealityAnalysis.estimated_profit.desc(),
        ).limit(limit)

        return list(self.session.execute(stmt).all())
