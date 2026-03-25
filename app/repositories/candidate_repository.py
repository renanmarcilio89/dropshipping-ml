from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.market import Candidate


class CandidateRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def upsert_candidates(self, terms: list[str]) -> int:
        now = datetime.now(timezone.utc)
        created_or_updated = 0

        for term in terms:
            normalized = self._normalize_term(term)

            stmt = select(Candidate).where(Candidate.normalized_term == normalized)
            existing = self.session.execute(stmt).scalars().first()

            if existing is None:
                row = Candidate(
                    source_term=term,
                    normalized_term=normalized,
                    candidate_type="product_term",
                    canonical_name=normalized,
                    status="pending_enrichment",
                    first_seen_at=now,
                    last_seen_at=now,
                )
                self.session.add(row)
                created_or_updated += 1
                continue

            existing.last_seen_at = now
            created_or_updated += 1

        self.session.commit()
        return created_or_updated

    @staticmethod
    def _normalize_term(term: str) -> str:
        normalized = " ".join(term.strip().lower().split())
        return normalized
