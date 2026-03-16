from app.repositories.search_repository import SearchRepository
from app.services.item_service import ItemService


class EnrichItemsJob:
    def __init__(self, service: ItemService, repository: SearchRepository) -> None:
        self.service = service
        self.repository = repository

    def run(self, site_id: str, item_ids: list[str]) -> dict:
        items, payload_hash, captured_at = self.service.enrich_items(item_ids=item_ids, site_id=site_id)
        for item in items:
            self.repository.save_item_snapshot(item=item, captured_at=captured_at, raw_payload_hash=payload_hash)
        return {
            'site_id': site_id,
            'captured_at': captured_at.isoformat(),
            'items_enriched': len(items),
            'raw_payload_hash': payload_hash,
        }
