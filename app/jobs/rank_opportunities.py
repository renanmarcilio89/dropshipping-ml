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

    def run(self, *, limit: int = 20) -> dict:
        rows = self.ranking_repository.list_top_opportunities(limit=limit)
        opportunities = self.ranking_service.build_output(rows)

        return {
            "count": len(opportunities),
            "items": opportunities,
        }
