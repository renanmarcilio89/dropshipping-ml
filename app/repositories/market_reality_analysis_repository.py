from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.market import MarketRealityAnalysis


class MarketRealityAnalysisRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, analysis: dict, *, analysis_version: str) -> MarketRealityAnalysis:
        record = MarketRealityAnalysis(
            candidate_id=analysis["candidate_id"],
            sale_price=analysis["sale_price"],
            supplier_cost=analysis["supplier_cost"],
            shipping_cost=analysis["shipping_cost"],
            marketplace_fee_rate=analysis["marketplace_fee_rate"],
            ads_cost_rate=analysis["ads_cost_rate"],
            marketplace_fee=analysis["marketplace_fee"],
            ads_cost=analysis["ads_cost"],
            total_cost=analysis["total_cost"],
            estimated_profit=analysis["estimated_profit"],
            estimated_margin=analysis["estimated_margin"],
            break_even_price=analysis["break_even_price"],
            viability_level=analysis["viability_level"],
            recommendation=analysis["recommendation"],
            analysis_version=analysis_version,
        )

        self.session.add(record)
        return record

    def list_latest(
        self,
        *,
        limit: int = 20,
        candidate_id: int | None = None,
        viability_level: str | None = None,
        min_estimated_margin: float | None = None,
        min_estimated_profit: float | None = None,
    ) -> list[MarketRealityAnalysis]:
        stmt = select(MarketRealityAnalysis)

        if candidate_id is not None:
            stmt = stmt.where(MarketRealityAnalysis.candidate_id == candidate_id)

        if viability_level is not None:
            stmt = stmt.where(MarketRealityAnalysis.viability_level == viability_level)

        if min_estimated_margin is not None:
            stmt = stmt.where(
                MarketRealityAnalysis.estimated_margin >= min_estimated_margin
            )

        if min_estimated_profit is not None:
            stmt = stmt.where(
                MarketRealityAnalysis.estimated_profit >= min_estimated_profit
            )

        stmt = stmt.order_by(
            MarketRealityAnalysis.created_at.desc(),
            MarketRealityAnalysis.estimated_margin.desc(),
            MarketRealityAnalysis.id.desc(),
        ).limit(limit)

        return list(self.session.scalars(stmt).all())
