from app.repositories.opportunity_ranking_repository import OpportunityRankingRepository
from app.services.opportunity_ranking_service import OpportunityRankingService
from app.services.commercial_opportunity_service import CommercialOpportunityService


class AnalyzeCommercialOpportunitiesJob:
    def __init__(
        self,
        *,
        ranking_repository: OpportunityRankingRepository,
        ranking_service: OpportunityRankingService,
        commercial_service: CommercialOpportunityService,
    ) -> None:
        self.ranking_repository = ranking_repository
        self.ranking_service = ranking_service
        self.commercial_service = commercial_service

    def run(self, *, limit: int = 20) -> dict:
        rows = self.ranking_repository.list_top_opportunities(limit=limit)
        opportunities = self.ranking_service.build_output(rows)

        analyzed = self.commercial_service.build_output(opportunities)

        return {
            "count": len(analyzed),
            "items": analyzed,
        }
