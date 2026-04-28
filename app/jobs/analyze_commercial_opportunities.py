from app.repositories.commercial_opportunity_analysis_repository import (
    CommercialOpportunityAnalysisRepository,
)
from app.repositories.opportunity_ranking_repository import OpportunityRankingRepository
from app.services.commercial_opportunity_service import CommercialOpportunityService
from app.services.market_price_service import MarketPriceService
from app.services.opportunity_ranking_service import OpportunityRankingService


class AnalyzeCommercialOpportunitiesJob:
    ANALYSIS_VERSION = "v1_commercial_structural"

    def __init__(
        self,
        *,
        ranking_repository: OpportunityRankingRepository,
        ranking_service: OpportunityRankingService,
        commercial_service: CommercialOpportunityService,
        analysis_repository: CommercialOpportunityAnalysisRepository,
    ) -> None:
        self.ranking_repository = ranking_repository
        self.ranking_service = ranking_service
        self.commercial_service = commercial_service
        self.analysis_repository = analysis_repository

    def run(self, *, limit: int = 20) -> dict:
        rows = self.ranking_repository.list_top_opportunities(limit=limit)
        opportunities = self.ranking_service.build_output(rows)

        price_service = MarketPriceService()

        enriched_opportunities = []
        for opportunity in opportunities:
            price_data = price_service.estimate_from_category(opportunity)
            opportunity.update(price_data)
            enriched_opportunities.append(opportunity)

        analyses = self.commercial_service.build_output(enriched_opportunities)
        self.analysis_repository.create_many(
            analyses,
            analysis_version=self.ANALYSIS_VERSION,
        )

        return {
            "count": len(analyses),
            "analysis_version": self.ANALYSIS_VERSION,
            "persisted": len(analyses),
            "items": analyses,
        }
