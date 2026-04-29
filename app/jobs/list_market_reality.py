from app.repositories.market_reality_analysis_repository import (
    MarketRealityAnalysisRepository,
)
from app.services.market_reality_query_service import MarketRealityQueryService


class ListMarketRealityJob:
    def __init__(
        self,
        *,
        analysis_repository: MarketRealityAnalysisRepository,
        query_service: MarketRealityQueryService,
    ) -> None:
        self.analysis_repository = analysis_repository
        self.query_service = query_service

    def run(
        self,
        *,
        limit: int = 20,
        candidate_id: int | None = None,
        viability_level: str | None = None,
        min_estimated_margin: float | None = None,
        min_estimated_profit: float | None = None,
    ) -> dict:
        normalized_viability_level = self.query_service.normalize_viability_level(
            viability_level
        )

        analyses = self.analysis_repository.list_latest(
            limit=limit,
            candidate_id=candidate_id,
            viability_level=normalized_viability_level,
            min_estimated_margin=min_estimated_margin,
            min_estimated_profit=min_estimated_profit,
        )

        items = self.query_service.build_output(analyses)

        return {
            "count": len(items),
            "filters": {
                "limit": limit,
                "candidate_id": candidate_id,
                "viability_level": normalized_viability_level,
                "min_estimated_margin": min_estimated_margin,
                "min_estimated_profit": min_estimated_profit,
            },
            "items": items,
        }
