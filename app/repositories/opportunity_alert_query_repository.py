from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.market import OpportunityAlert


class OpportunityAlertQueryRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_alerts(
        self,
        *,
        limit: int = 50,
        status: str | None = None,
        min_final_score: float | None = None,
        confidence_level: str | None = None,
    ) -> list[OpportunityAlert]:
        stmt = select(OpportunityAlert)

        if status is not None:
            stmt = stmt.where(OpportunityAlert.status == status)

        if min_final_score is not None:
            stmt = stmt.where(OpportunityAlert.final_score >= min_final_score)

        if confidence_level is not None:
            stmt = stmt.where(OpportunityAlert.confidence_level == confidence_level)

        stmt = stmt.order_by(
            OpportunityAlert.created_at.desc(),
            OpportunityAlert.id.desc(),
        ).limit(limit)

        return list(self.session.execute(stmt).scalars().all())
