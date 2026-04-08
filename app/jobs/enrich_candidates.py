from app.repositories.candidate_market_snapshot_repository import CandidateMarketSnapshotRepository
from app.repositories.candidate_repository import CandidateRepository
from app.repositories.raw_payload_repository import RawPayloadRepository
from app.services.candidate_enrichment_service import CandidateEnrichmentService


class EnrichCandidatesJob:
    def __init__(
        self,
        *,
        candidate_repository: CandidateRepository,
        snapshot_repository: CandidateMarketSnapshotRepository,
        raw_payload_repository: RawPayloadRepository,
        enrichment_service: CandidateEnrichmentService,
    ) -> None:
        self.candidate_repository = candidate_repository
        self.snapshot_repository = snapshot_repository
        self.raw_payload_repository = raw_payload_repository
        self.enrichment_service = enrichment_service

    def run(self, *, site_id: str, limit: int = 20) -> dict:
        session = self.candidate_repository.session

        candidates = self.candidate_repository.list_ready_for_enrichment(limit=limit)

        enriched = 0
        failed = 0

        for candidate in candidates:
            try:
                result = self.enrichment_service.enrich(
                    query=candidate.normalized_term,
                    site_id=site_id,
                )

                self.raw_payload_repository.save(
                    source_name="domain_discovery",
                    endpoint=f"/sites/{site_id}/domain_discovery/search",
                    payload=result.prediction_payload,
                    payload_hash=self.enrichment_service.payload_hash(result.prediction_payload),
                    captured_at=result.captured_at,
                    request_params={"q": candidate.normalized_term, "limit": 3},
                    site_id=site_id,
                )

                if result.category_payload is not None and result.predicted_category_id is not None:
                    self.raw_payload_repository.save(
                        source_name="category_detail",
                        endpoint=f"/categories/{result.predicted_category_id}",
                        payload=result.category_payload,
                        payload_hash=self.enrichment_service.payload_hash(result.category_payload),
                        captured_at=result.captured_at,
                        request_params=None,
                        site_id=site_id,
                    )

                if result.category_attributes_payload and result.predicted_category_id is not None:
                    self.raw_payload_repository.save(
                        source_name="category_attributes",
                        endpoint=f"/categories/{result.predicted_category_id}/attributes",
                        payload=result.category_attributes_payload,
                        payload_hash=self.enrichment_service.payload_hash(result.category_attributes_payload),
                        captured_at=result.captured_at,
                        request_params=None,
                        site_id=site_id,
                    )

                self.snapshot_repository.save(
                    candidate_id=candidate.id,
                    site_id=site_id,
                    query_term=candidate.normalized_term,
                    prediction_found=result.prediction_found,
                    predicted_domain_id=result.predicted_domain_id,
                    predicted_domain_name=result.predicted_domain_name,
                    predicted_category_id=result.predicted_category_id,
                    predicted_category_name=result.predicted_category_name,
                    predicted_attributes_count=result.predicted_attributes_count,
                    predicted_attributes=result.predicted_attributes,
                    category_path=result.category_path,
                    category_path_text=result.category_path_text,
                    category_depth=result.category_depth,
                    category_total_items=result.category_total_items,
                    catalog_domain=result.catalog_domain,
                    listing_allowed=result.listing_allowed,
                    buying_modes=result.buying_modes,
                    required_attributes_count=result.required_attributes_count,
                    important_attributes_count=result.important_attributes_count,
                    attribute_types_summary=result.attribute_types_summary,
                    top_relevant_attributes=result.top_relevant_attributes,
                    term_token_count=result.term_token_count,
                    term_specificity_level=result.term_specificity_level,
                    prediction_confidence_score=result.prediction_confidence_score,
                    prediction_confidence_level=result.prediction_confidence_level,
                    captured_at=result.captured_at,
                )

                self.candidate_repository.mark_enriched(
                    candidate,
                    enriched_at=result.captured_at,
                    reason="enriquecimento estrutural concluido com sucesso",
                )

                session.commit()
                enriched += 1
            except Exception as exc:
                session.rollback()
                self.candidate_repository.mark_enrichment_failed(
                    candidate,
                    reason=str(exc),
                )
                session.commit()
                failed += 1

        return {
            "candidates_read": len(candidates),
            "enriched": enriched,
            "failed": failed,
        }
