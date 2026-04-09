from app.repositories.opportunity_ranking_repository import OpportunityRankingRepository
from app.services.opportunity_alert_service import OpportunityAlertService
from app.services.opportunity_ranking_service import OpportunityRankingService


class AlertOpportunitiesJob:
    def __init__(
        self,
        *,
        ranking_repository: OpportunityRankingRepository,
        ranking_service: OpportunityRankingService,
        alert_service: OpportunityAlertService,
    ) -> None:
        self.ranking_repository = ranking_repository
        self.ranking_service = ranking_service
        self.alert_service = alert_service

    def run(self, *, limit: int = 50) -> dict:
        rows = self.ranking_repository.list_top_opportunities(limit=limit)
        items = self.ranking_service.build_output(rows)

        alerts = []

        for item in items:
            alert = self.alert_service.evaluate(item)
            if alert:
                alerts.append(alert)

        return {
            "candidates_evaluated": len(items),
            "alerts_generated": len(alerts),
            "alerts": alerts,
        }
