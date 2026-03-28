from datetime import datetime
from sqlalchemy.orm import Session

from app.models.market import CandidateMarketSnapshot


class CandidateMarketSnapshotRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(
        self,
        *,
        candidate_id: int,
        site_id: str,
        query_term: str,
        predicted_domain_id: str | None,
        predicted_domain_name: str | None,
        predicted_category_id: str | None,
        predicted_category_name: str | None,
        search_total: int | None,
        sample_size: int,
        unique_seller_count: int,
        price_min: float | None,
        price_max: float | None,
        price_avg: float | None,
        price_median: float | None,
        free_shipping_ratio: float | None,
        catalog_listing_ratio: float | None,
        official_store_ratio: float | None,
        new_condition_ratio: float | None,
        category_total_items: int | None,
        captured_at: datetime,
    ) -> CandidateMarketSnapshot:
        row = CandidateMarketSnapshot(
            candidate_id=candidate_id,
            site_id=site_id,
            query_term=query_term,
            predicted_domain_id=predicted_domain_id,
            predicted_domain_name=predicted_domain_name,
            predicted_category_id=predicted_category_id,
            predicted_category_name=predicted_category_name,
            search_total=search_total,
            sample_size=sample_size,
            unique_seller_count=unique_seller_count,
            price_min=price_min,
            price_max=price_max,
            price_avg=price_avg,
            price_median=price_median,
            free_shipping_ratio=free_shipping_ratio,
            catalog_listing_ratio=catalog_listing_ratio,
            official_store_ratio=official_store_ratio,
            new_condition_ratio=new_condition_ratio,
            category_total_items=category_total_items,
            captured_at=captured_at,
        )
        self.session.add(row)
        self.session.flush()
        self.session.refresh(row)
        return row
