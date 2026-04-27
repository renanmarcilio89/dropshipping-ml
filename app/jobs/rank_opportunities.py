from app.repositories.opportunity_ranking_repository import OpportunityRankingRepository
from app.services.opportunity_ranking_service import OpportunityRankingService


class RankOpportunitiesJob:
    def __init__(
        self,
        *,
        ranking_repository: OpportunityRankingRepository,
        ranking_service: OpportunityRankingService,
    ) -> None:
        self.ranking_repository = ranking_repository
        self.ranking_service = ranking_service

    def run(
        self,
        *,
        limit: int = 20,
        min_final_score: float | None = None,
        confidence_level: str | None = None,
        listing_allowed: bool | None = None,
        max_category_total_items: int | None = None,
    ) -> dict:
        normalized_confidence_level = self.ranking_service.normalize_confidence_level(
            confidence_level
        )

        rows = self.ranking_repository.list_top_opportunities(
            limit=limit,
            min_final_score=min_final_score,
            confidence_level=normalized_confidence_level,
            listing_allowed=listing_allowed,
            max_category_total_items=max_category_total_items,
        )
        opportunities = self.ranking_service.build_output(rows)

        return {
            "count": len(opportunities),
            "filters": {
                "limit": limit,
                "min_final_score": min_final_score,
                "confidence_level": normalized_confidence_level,
                "listing_allowed": listing_allowed,
                "max_category_total_items": max_category_total_items,
            },
            "items": opportunities,
        }
