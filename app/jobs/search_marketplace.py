from app.repositories.search_repository import SearchRepository
from app.services.search_service import SearchService


class SearchMarketplaceJob:
    def __init__(self, service: SearchService, repository: SearchRepository) -> None:
        self.service = service
        self.repository = repository

    def run(self, site_id: str, query: str, offset: int = 0) -> dict:
        items, payload_hash, captured_at = self.service.search_marketplace(
            query=query,
            site_id=site_id,
            offset=offset,
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
        }
