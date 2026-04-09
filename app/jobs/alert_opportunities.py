from datetime import datetime, timezone

from app.repositories.opportunity_alert_repository import OpportunityAlertRepository
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
        alert_repository: OpportunityAlertRepository,
    ) -> None:
        self.ranking_repository = ranking_repository
        self.ranking_service = ranking_service
        self.alert_service = alert_service
        self.alert_repository = alert_repository

    def run(self, *, limit: int = 50) -> dict:
        rows = self.ranking_repository.list_top_opportunities(limit=limit)
        items = self.ranking_service.build_output(rows)

        created = 0
        duplicated = 0
        alerts_output = []

        for item in items:
            alert = self.alert_service.evaluate(item)
            if alert is None:
                continue

            existing = self.alert_repository.get_by_hash(alert["alert_hash"])
            if existing is not None:
                duplicated += 1
                continue

            row = self.alert_repository.save(
                candidate_id=alert["candidate_id"],
                alert_hash=alert["alert_hash"],
                alert_version=alert["alert_version"],
                score_version=alert.get("score_version"),
                final_score=float(alert["final_score"]),
                confidence_level=alert.get("confidence"),
                category_id=alert.get("predicted_category_id"),
                category_name=alert.get("category"),
                action=alert["action"],
                reason_payload=alert["reasons"],
                status="open",
                created_at=datetime.now(timezone.utc),
            )

            alerts_output.append(
                {
                    "alert_id": row.id,
                    "candidate_id": alert["candidate_id"],
                    "term": alert["term"],
                    "category": alert.get("category"),
                    "final_score": alert["final_score"],
                    "confidence": alert.get("confidence"),
                    "reasons": alert["reasons"],
                    "action": alert["action"],
                    "status": row.status,
                    "created_at": row.created_at.isoformat() if row.created_at else None,
                }
            )
            created += 1

        return {
            "candidates_evaluated": len(items),
            "alerts_created": created,
            "alerts_duplicated": duplicated,
            "alerts": alerts_output,
        }
