from app.repositories.investment_priority_repository import InvestmentPriorityRepository
from app.services.commercial_opportunity_query_service import (
    CommercialOpportunityQueryService,
)
from app.services.investment_priority_service import InvestmentPriorityService
from app.services.market_reality_query_service import MarketRealityQueryService


class ListInvestmentPrioritiesJob:
    def __init__(
        self,
        *,
        priority_repository: InvestmentPriorityRepository,
        priority_service: InvestmentPriorityService,
        commercial_query_service: CommercialOpportunityQueryService,
        market_reality_query_service: MarketRealityQueryService,
    ) -> None:
        self.priority_repository = priority_repository
        self.priority_service = priority_service
        self.commercial_query_service = commercial_query_service
        self.market_reality_query_service = market_reality_query_service

    def run(
        self,
        *,
        limit: int = 20,
        min_final_score: float | None = None,
        min_commercial_score: float | None = None,
        min_estimated_margin: float | None = None,
        commercial_decision: str | None = None,
        viability_level: str | None = None,
    ) -> dict:
        normalized_commercial_decision = (
            self.commercial_query_service.normalize_commercial_decision(
                commercial_decision
            )
        )
        normalized_viability_level = (
            self.market_reality_query_service.normalize_viability_level(
                viability_level
            )
        )

        rows = self.priority_repository.list_priorities(
            limit=limit,
            min_final_score=min_final_score,
            min_commercial_score=min_commercial_score,
            min_estimated_margin=min_estimated_margin,
            commercial_decision=normalized_commercial_decision,
            viability_level=normalized_viability_level,
        )

        items = self.priority_service.build_output(rows)

        return {
            "count": len(items),
            "filters": {
                "limit": limit,
                "min_final_score": min_final_score,
                "min_commercial_score": min_commercial_score,
                "min_estimated_margin": min_estimated_margin,
                "commercial_decision": normalized_commercial_decision,
                "viability_level": normalized_viability_level,
            },
            "items": items,
        }
