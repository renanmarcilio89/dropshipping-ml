from app.repositories.candidate_repository import CandidateRepository
from app.services.candidate_qualification_service import CandidateQualificationService


class QualifyCandidatesJob:
    def __init__(
        self,
        candidate_repository: CandidateRepository,
        qualification_service: CandidateQualificationService,
    ) -> None:
        self.candidate_repository = candidate_repository
        self.qualification_service = qualification_service

    def run(self, limit: int = 100) -> dict:
        candidates = self.candidate_repository.list_pending_qualification(limit=limit)

        approved = 0
        rejected = 0
        needs_review = 0

        for candidate in candidates:
            decision = self.qualification_service.qualify(candidate.normalized_term)

            self.candidate_repository.apply_qualification(
                candidate,
                qualification_status=decision.qualification_status,
                qualification_reason=decision.reason,
            )

            if decision.qualification_status == "approved":
                approved += 1
            elif decision.qualification_status == "rejected":
                rejected += 1
            else:
                needs_review += 1

        self.candidate_repository.commit()

        return {
            "candidates_read": len(candidates),
            "approved": approved,
            "rejected": rejected,
            "needs_review": needs_review,
        }
