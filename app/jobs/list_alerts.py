from app.repositories.opportunity_alert_query_repository import OpportunityAlertQueryRepository
from app.services.opportunity_alert_query_service import OpportunityAlertQueryService


class ListAlertsJob:
    def __init__(
        self,
        *,
        alert_query_repository: OpportunityAlertQueryRepository,
        alert_query_service: OpportunityAlertQueryService,
    ) -> None:
        self.alert_query_repository = alert_query_repository
        self.alert_query_service = alert_query_service

    def run(
        self,
        *,
        limit: int = 50,
        status: str | None = None,
        min_final_score: float | None = None,
        confidence_level: str | None = None,
    ) -> dict:
        normalized_status = self.alert_query_service.normalize_status(status)
        normalized_confidence = self.alert_query_service.normalize_confidence_level(
            confidence_level
        )

        rows = self.alert_query_repository.list_alerts(
            limit=limit,
            status=normalized_status,
            min_final_score=min_final_score,
            confidence_level=normalized_confidence,
        )

        items = self.alert_query_service.build_output(rows)

        return {
            "count": len(items),
            "filters": {
                "limit": limit,
                "status": normalized_status,
                "min_final_score": min_final_score,
                "confidence_level": normalized_confidence,
            },
            "items": items,
        }
