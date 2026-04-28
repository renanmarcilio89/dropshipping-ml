from app.repositories.commercial_opportunity_analysis_repository import (
    CommercialOpportunityAnalysisRepository,
)
from app.services.commercial_opportunity_query_service import (
    CommercialOpportunityQueryService,
)


class ListCommercialAnalysesJob:
    def __init__(
        self,
        *,
        analysis_repository: CommercialOpportunityAnalysisRepository,
        query_service: CommercialOpportunityQueryService,
    ) -> None:
        self.analysis_repository = analysis_repository
        self.query_service = query_service

    def run(
        self,
        *,
        limit: int = 20,
        commercial_decision: str | None = None,
        risk_level: str | None = None,
        min_commercial_score: float | None = None,
    ) -> dict:
        normalized_decision = self.query_service.normalize_commercial_decision(
            commercial_decision
        )
        normalized_risk_level = self.query_service.normalize_risk_level(risk_level)

        analyses = self.analysis_repository.list_latest(
            limit=limit,
            commercial_decision=normalized_decision,
            risk_level=normalized_risk_level,
            min_commercial_score=min_commercial_score,
        )

        items = self.query_service.build_output(analyses)

        return {
            "count": len(items),
            "filters": {
                "limit": limit,
                "commercial_decision": normalized_decision,
                "risk_level": normalized_risk_level,
                "min_commercial_score": min_commercial_score,
            },
            "items": items,
        }
