from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
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
        prediction_found: bool,
        predicted_domain_id: str | None,
        predicted_domain_name: str | None,
        predicted_category_id: str | None,
        predicted_category_name: str | None,
        predicted_attributes_count: int,
        predicted_attributes: list[dict] | None,
        category_path: list[dict] | None,
        category_path_text: str | None,
        category_depth: int | None,
        category_total_items: int | None,
        catalog_domain: str | None,
        listing_allowed: bool | None,
        buying_modes: list[str] | None,
        required_attributes_count: int,
        important_attributes_count: int,
        attribute_types_summary: dict | None,
        top_relevant_attributes: list[dict] | None,
        term_token_count: int,
        term_specificity_level: str,
        prediction_confidence_score: float | None,
        prediction_confidence_level: str | None,
        captured_at: datetime,
    ) -> CandidateMarketSnapshot:
        row = CandidateMarketSnapshot(
            candidate_id=candidate_id,
            site_id=site_id,
            query_term=query_term,
            prediction_found=prediction_found,
            predicted_domain_id=predicted_domain_id,
            predicted_domain_name=predicted_domain_name,
            predicted_category_id=predicted_category_id,
            predicted_category_name=predicted_category_name,
            predicted_attributes_count=predicted_attributes_count,
            predicted_attributes=predicted_attributes,
            category_path=category_path,
            category_path_text=category_path_text,
            category_depth=category_depth,
            category_total_items=category_total_items,
            catalog_domain=catalog_domain,
            listing_allowed=listing_allowed,
            buying_modes=buying_modes,
            required_attributes_count=required_attributes_count,
            important_attributes_count=important_attributes_count,
            attribute_types_summary=attribute_types_summary,
            top_relevant_attributes=top_relevant_attributes,
            term_token_count=term_token_count,
            term_specificity_level=term_specificity_level,
            prediction_confidence_score=prediction_confidence_score,
            prediction_confidence_level=prediction_confidence_level,
            captured_at=captured_at,
        )
        self.session.add(row)
        self.session.flush()
        self.session.refresh(row)
        return row

    def get_latest_by_candidate_id(self, candidate_id: int) -> CandidateMarketSnapshot | None:
        stmt = (
            select(CandidateMarketSnapshot)
            .where(CandidateMarketSnapshot.candidate_id == candidate_id)
            .order_by(
                CandidateMarketSnapshot.captured_at.desc(),
                CandidateMarketSnapshot.id.desc(),
            )
        )
        return self.session.execute(stmt).scalars().first()
