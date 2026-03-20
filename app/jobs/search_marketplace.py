from app.repositories.raw_payload_repository import RawPayloadRepository
from app.repositories.search_repository import SearchRepository
from app.services.search_service import SearchService


class SearchMarketplaceJob:
    def __init__(
        self,
        service: SearchService,
        repository: SearchRepository,
        raw_payload_repository: RawPayloadRepository,
    ) -> None:
        self.service = service
        self.repository = repository
        self.raw_payload_repository = raw_payload_repository

    def run(self, site_id: str, query: str, offset: int = 0) -> dict:
        items, payload, payload_hash, captured_at = self.service.search_marketplace(
            query=query,
            site_id=site_id,
            offset=offset,
        )

        raw_payload = self.raw_payload_repository.save(
            source_name='search',
            endpoint=f'/sites/{site_id}/search',
            payload=payload,
            payload_hash=payload_hash,
            captured_at=captured_at,
            request_params={'q': query, 'offset': offset},
            site_id=site_id,
        )

        saved = self.repository.save_search_results(
            site_id=site_id,
            query=query,
            items=items,
            captured_at=captured_at,
            offset=offset,
            raw_payload_hash=payload_hash,
        )

        return {
            'site_id': site_id,
            'query': query,
            'offset': offset,
            'captured_at': captured_at.isoformat(),
            'saved_results': saved,
            'item_ids': [item.item_id for item in items],
            'raw_payload_hash': payload_hash,
            'raw_payload_id': raw_payload.id,
        }
