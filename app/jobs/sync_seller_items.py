from app.repositories.raw_payload_repository import RawPayloadRepository
from app.repositories.search_repository import SearchRepository
from app.services.item_service import ItemService
from app.services.search_service import SearchService


class SyncSellerItemsJob:
    def __init__(
        self,
        search_service: SearchService,
        item_service: ItemService,
        search_repository: SearchRepository,
        raw_payload_repository: RawPayloadRepository,
    ) -> None:
        self.search_service = search_service
        self.item_service = item_service
        self.search_repository = search_repository
        self.raw_payload_repository = raw_payload_repository

    def run(
        self,
        *,
        user_id: int,
        site_id: str,
        offset: int = 0,
        limit: int = 50,
        search_type: str | None = None,
        extra_params: dict | None = None,
    ) -> dict:
        item_ids, search_payload, search_payload_hash, captured_at = (
            self.search_service.search_user_items(
                user_id=user_id,
                offset=offset,
                limit=limit,
                search_type=search_type,
                extra_params=extra_params,
            )
        )

        self.raw_payload_repository.save(
            source_name="meli_user_items_search",
            endpoint=f"/users/{user_id}/items/search",
            payload=search_payload,
            payload_hash=search_payload_hash,
            captured_at=captured_at,
            request_params={
                "offset": offset,
                "limit": limit,
                "search_type": search_type,
                **(extra_params or {}),
            },
            site_id=site_id,
        )

        if not item_ids:
            return {
                "user_id": user_id,
                "site_id": site_id,
                "captured_at": captured_at.isoformat(),
                "items_found": 0,
                "items_enriched": 0,
                "raw_payload_hash": search_payload_hash,
            }

        items, items_payload_hash, items_captured_at = self.item_service.enrich_items(
            item_ids=item_ids,
            site_id=site_id,
        )

        for item in items:
            self.search_repository.save_item_snapshot(
                item=item,
                captured_at=items_captured_at,
                raw_payload_hash=items_payload_hash,
            )

        return {
            "user_id": user_id,
            "site_id": site_id,
            "captured_at": captured_at.isoformat(),
            "items_found": len(item_ids),
            "items_enriched": len(items),
            "item_ids": item_ids,
            "search_payload_hash": search_payload_hash,
            "items_payload_hash": items_payload_hash,
        }
