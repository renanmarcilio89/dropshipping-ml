from app.repositories.raw_payload_repository import RawPayloadRepository
from app.repositories.search_repository import SearchRepository
from app.services.search_service import SearchService


class SyncTrendsJob:
    def __init__(
        self,
        service: SearchService,
        repository: SearchRepository,
        raw_payload_repository: RawPayloadRepository,
    ) -> None:
        self.service = service
        self.repository = repository
        self.raw_payload_repository = raw_payload_repository

    def run(self, site_id: str) -> dict:
        terms, payload, payload_hash, captured_at = self.service.fetch_trends(site_id)

        raw_payload = self.raw_payload_repository.save(
            source_name='trends',
            endpoint=f'/trends/{site_id}',
            payload=payload,
            payload_hash=payload_hash,
            captured_at=captured_at,
            request_params=None,
            site_id=site_id,
        )

        saved = self.repository.save_trends(site_id=site_id, terms=terms, captured_at=captured_at)

        return {
            'site_id': site_id,
            'captured_at': captured_at.isoformat(),
            'saved_terms': saved,
            'raw_payload_hash': payload_hash,
            'raw_payload_id': raw_payload.id,
        }
