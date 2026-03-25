from app.repositories.candidate_repository import CandidateRepository
from app.repositories.trend_repository import TrendRepository
from app.services.candidate_service import CandidateService


class BuildCandidatesJob:
    def __init__(
        self,
        trend_repository: TrendRepository,
        candidate_repository: CandidateRepository,
        candidate_service: CandidateService,
    ) -> None:
        self.trend_repository = trend_repository
        self.candidate_repository = candidate_repository
        self.candidate_service = candidate_service

    def run(self, trend_limit: int = 100) -> dict:
        terms = self.trend_repository.list_recent_terms(limit=trend_limit)
        prepared_terms = self.candidate_service.build_from_terms(terms)
        saved = self.candidate_repository.upsert_candidates(prepared_terms)

        return {
            "trend_terms_read": len(terms),
            "candidate_terms_prepared": len(prepared_terms),
            "candidates_created_or_updated": saved,
        }
