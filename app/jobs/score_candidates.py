from app.repositories.candidate_market_snapshot_repository import CandidateMarketSnapshotRepository
from app.repositories.candidate_repository import CandidateRepository
from app.repositories.opportunity_score_repository import OpportunityScoreRepository
from app.services.opportunity_scoring_service import OpportunityScoringService


class ScoreCandidatesJob:
    def __init__(
        self,
        *,
        candidate_repository: CandidateRepository,
        snapshot_repository: CandidateMarketSnapshotRepository,
        opportunity_score_repository: OpportunityScoreRepository,
        scoring_service: OpportunityScoringService,
    ) -> None:
        self.candidate_repository = candidate_repository
        self.snapshot_repository = snapshot_repository
        self.opportunity_score_repository = opportunity_score_repository
        self.scoring_service = scoring_service

    def run(self, *, limit: int = 100) -> dict:
        session = self.candidate_repository.session
        candidates = self.candidate_repository.list_ready_for_scoring(limit=limit)

        scored = 0
        skipped = 0
        failed = 0

        for candidate in candidates:
            try:
                snapshot = self.snapshot_repository.get_latest_by_candidate_id(candidate.id)

                if snapshot is None:
                    skipped += 1
                    continue

                result = self.scoring_service.score(snapshot)

                self.opportunity_score_repository.save(
                    candidate_id=candidate.id,
                    demand_score=result.demand_score,
                    competition_score=result.competition_score,
                    quality_score=result.quality_score,
                    ops_risk_score=result.ops_risk_score,
                    final_score=result.final_score,
                    score_version=result.score_version,
                    captured_at=result.captured_at,
                )

                session.commit()
                scored += 1
            except Exception:
                session.rollback()
                failed += 1

        return {
            "candidates_read": len(candidates),
            "scored": scored,
            "skipped": skipped,
            "failed": failed,
        }
