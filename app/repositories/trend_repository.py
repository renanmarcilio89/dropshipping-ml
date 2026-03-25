from datetime import datetime

from sqlalchemy.orm import Session

from app.models.market import TrendSnapshot


class TrendRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save_trends(
        self,
        *,
        site_id: str,
        terms: list[str],
        captured_at: datetime,
        raw_payload_hash: str | None = None,
    ) -> int:
        rows = [
            TrendSnapshot(
                site_id=site_id,
                term=term,
                rank_position=index + 1,
                raw_payload_hash=raw_payload_hash,
                captured_at=captured_at,
            )
            for index, term in enumerate(terms)
        ]

        self.session.add_all(rows)
        self.session.commit()
        return len(rows)
