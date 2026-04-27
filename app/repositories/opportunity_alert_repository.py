from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.market import OpportunityAlert


class OpportunityAlertRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_by_hash(self, alert_hash: str) -> OpportunityAlert | None:
        stmt = select(OpportunityAlert).where(OpportunityAlert.alert_hash == alert_hash)
        return self.session.execute(stmt).scalars().first()

    def save(
        self,
        *,
        candidate_id: int,
        alert_hash: str,
        alert_version: str,
        score_version: str | None,
        final_score: float,
        confidence_level: str | None,
        category_id: str | None,
        category_name: str | None,
        action: str,
        reason_payload: list[str],
        status: str,
        created_at: datetime,
    ) -> OpportunityAlert:
        existing = self.get_by_hash(alert_hash)
        if existing is not None:
            return existing

        row = OpportunityAlert(
            candidate_id=candidate_id,
            alert_hash=alert_hash,
            alert_version=alert_version,
            score_version=score_version,
            final_score=final_score,
            confidence_level=confidence_level,
            category_id=category_id,
            category_name=category_name,
            action=action,
            reason_payload=reason_payload,
            status=status,
            created_at=created_at,
        )
        self.session.add(row)
        self.session.flush()
        self.session.refresh(row)
        return row
