from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.candidate_status import CandidateQualificationStatus, CandidateStatus
from app.core.text_normalization import normalize_term
from app.models.market import Candidate


class CandidateRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def list_enrichment_targets(self, limit: int = 100, force: bool = False) -> list[Candidate]:
        if not force:
            return self.list_ready_for_enrichment(limit=limit)

        stmt = (
            select(Candidate)
            .where(
                Candidate.status.in_(
                    [
                        CandidateStatus.APPROVED_FOR_ENRICHMENT,
                        CandidateStatus.ENRICHED,
                        CandidateStatus.ENRICHMENT_FAILED,
                    ]
                )
            )
            .order_by(Candidate.last_enriched_at.asc().nullsfirst(), Candidate.id.asc())
            .limit(limit)
        )
        return list(self.session.execute(stmt).scalars().all())

    def list_scoring_targets(self, limit: int = 100, force: bool = False) -> list[Candidate]:
        if not force:
            return self.list_ready_for_scoring(limit=limit)

        stmt = (
            select(Candidate)
            .where(Candidate.last_enriched_at.is_not(None))
            .order_by(Candidate.last_enriched_at.asc(), Candidate.id.asc())
            .limit(limit)
        )
        return list(self.session.execute(stmt).scalars().all())

    def upsert_candidates(self, terms: list[str]) -> int:
        now = datetime.now(timezone.utc)
        created_or_updated = 0

        for term in terms:
            normalized = normalize_term(term)

            stmt = select(Candidate).where(Candidate.normalized_term == normalized)
            existing = self.session.execute(stmt).scalars().first()

            if existing is None:
                row = Candidate(
                    source_term=term,
                    normalized_term=normalized,
                    candidate_type="product_term",
                    canonical_name=normalized,
                    status=CandidateStatus.PENDING_ENRICHMENT,
                    qualification_status=CandidateQualificationStatus.PENDING,
                    first_seen_at=now,
                    last_seen_at=now,
                )
                self.session.add(row)
                created_or_updated += 1
                continue

            existing.last_seen_at = now
            created_or_updated += 1

        return created_or_updated

    def list_pending_qualification(self, limit: int = 100) -> list[Candidate]:
        stmt = (
            select(Candidate)
            .where(Candidate.qualification_status == CandidateQualificationStatus.PENDING)
            .order_by(Candidate.id.asc())
            .limit(limit)
        )
        return list(self.session.execute(stmt).scalars().all())

    def apply_qualification(
        self,
        candidate: Candidate,
        *,
        qualification_status: str,
        qualification_reason: str,
    ) -> None:
        now = datetime.now(timezone.utc)

        candidate.qualification_status = qualification_status
        candidate.qualification_reason = qualification_reason
        candidate.last_qualified_at = now

        if qualification_status == CandidateQualificationStatus.APPROVED:
            candidate.status = CandidateStatus.APPROVED_FOR_ENRICHMENT
        elif qualification_status == CandidateQualificationStatus.REJECTED:
            candidate.status = CandidateStatus.REJECTED
        else:
            candidate.status = CandidateStatus.NEEDS_REVIEW

    def list_ready_for_enrichment(self, limit: int = 100) -> list[Candidate]:
        stmt = (
            select(Candidate)
            .where(Candidate.status == CandidateStatus.APPROVED_FOR_ENRICHMENT)
            .order_by(Candidate.id.asc())
            .limit(limit)
        )
        return list(self.session.execute(stmt).scalars().all())

    def list_ready_for_scoring(self, limit: int = 100) -> list[Candidate]:
        stmt = (
            select(Candidate)
            .where(Candidate.status == CandidateStatus.ENRICHED)
            .order_by(Candidate.id.asc())
            .limit(limit)
        )
        return list(self.session.execute(stmt).scalars().all())

    def mark_enriched(
        self,
        candidate: Candidate,
        *,
        enriched_at: datetime,
        reason: str,
    ) -> None:
        candidate.status = CandidateStatus.ENRICHED
        candidate.last_enriched_at = enriched_at
        candidate.enrichment_reason = reason

    def mark_enrichment_failed(
        self,
        candidate: Candidate,
        *,
        reason: str,
    ) -> None:
        candidate.status = CandidateStatus.ENRICHMENT_FAILED
        candidate.enrichment_reason = reason
