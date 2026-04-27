from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, JSON, Numeric, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.candidate_status import CandidateQualificationStatus, CandidateStatus, CandidateType
from app.models.base import Base


class TrendSnapshot(Base):
    __tablename__ = "trend_snapshot"
    __table_args__ = (
        Index("ix_trend_snapshot_captured_at", "captured_at"),
        Index("ix_trend_snapshot_site_id_captured_at", "site_id", "captured_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    site_id: Mapped[str] = mapped_column(Text, nullable=False)
    term: Mapped[str] = mapped_column(Text, nullable=False)
    rank_position: Mapped[int] = mapped_column(nullable=False)
    raw_payload_hash: Mapped[str | None] = mapped_column(Text, nullable=True)
    captured_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class Candidate(Base):
    __tablename__ = "candidate"
    __table_args__ = (
        UniqueConstraint("normalized_term", name="uq_candidate_normalized_term"),
        Index("ix_candidate_status", "status"),
        Index("ix_candidate_qualification_status", "qualification_status"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    source_term: Mapped[str] = mapped_column(Text, nullable=False)
    normalized_term: Mapped[str] = mapped_column(Text, nullable=False)
    candidate_type: Mapped[str] = mapped_column(Text, nullable=False, default=CandidateType.PRODUCT_TERM)
    canonical_name: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False, default=CandidateStatus.PENDING_ENRICHMENT)
    qualification_status: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        default=CandidateQualificationStatus.PENDING,
    )
    qualification_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    last_qualified_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    last_enriched_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    enrichment_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    first_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class CandidateMarketSnapshot(Base):
    __tablename__ = "candidate_market_snapshot"
    __table_args__ = (
        Index("ix_candidate_market_snapshot_candidate_id", "candidate_id"),
        Index("ix_candidate_market_snapshot_captured_at", "captured_at"),
        Index("ix_candidate_market_snapshot_predicted_category_id", "predicted_category_id"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidate.id"), nullable=False)
    site_id: Mapped[str] = mapped_column(Text, nullable=False)
    query_term: Mapped[str] = mapped_column(Text, nullable=False)

    prediction_found: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    predicted_domain_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    predicted_domain_name: Mapped[str | None] = mapped_column(Text, nullable=True)
    predicted_category_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    predicted_category_name: Mapped[str | None] = mapped_column(Text, nullable=True)

    predicted_attributes_count: Mapped[int] = mapped_column(nullable=False, default=0)
    predicted_attributes: Mapped[list | None] = mapped_column(JSON, nullable=True)

    category_path: Mapped[list | None] = mapped_column(JSON, nullable=True)
    category_path_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    category_depth: Mapped[int | None] = mapped_column(nullable=True)
    category_total_items: Mapped[int | None] = mapped_column(nullable=True)

    catalog_domain: Mapped[str | None] = mapped_column(Text, nullable=True)
    listing_allowed: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    buying_modes: Mapped[list | None] = mapped_column(JSON, nullable=True)

    required_attributes_count: Mapped[int] = mapped_column(nullable=False, default=0)
    important_attributes_count: Mapped[int] = mapped_column(nullable=False, default=0)
    attribute_types_summary: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    top_relevant_attributes: Mapped[list | None] = mapped_column(JSON, nullable=True)

    term_token_count: Mapped[int] = mapped_column(nullable=False, default=0)
    term_specificity_level: Mapped[str] = mapped_column(Text, nullable=False, default="low")

    prediction_confidence_score: Mapped[float | None] = mapped_column(Numeric(8, 4), nullable=True)
    prediction_confidence_level: Mapped[str | None] = mapped_column(Text, nullable=True)

    captured_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class OpportunityScore(Base):
    __tablename__ = "opportunity_score"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidate.id"), nullable=False)
    demand_score: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    competition_score: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    quality_score: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    ops_risk_score: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    final_score: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    score_version: Mapped[str] = mapped_column(Text, nullable=False)
    captured_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )


class OpportunityAlert(Base):
    __tablename__ = "opportunity_alert"
    __table_args__ = (
        UniqueConstraint("alert_hash", name="uq_opportunity_alert_alert_hash"),
        Index("ix_opportunity_alert_candidate_id", "candidate_id"),
        Index("ix_opportunity_alert_status", "status"),
        Index("ix_opportunity_alert_created_at", "created_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidate.id"), nullable=False)

    alert_hash: Mapped[str] = mapped_column(Text, nullable=False)
    alert_version: Mapped[str] = mapped_column(Text, nullable=False)
    score_version: Mapped[str | None] = mapped_column(Text, nullable=True)

    final_score: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    confidence_level: Mapped[str | None] = mapped_column(Text, nullable=True)

    category_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    category_name: Mapped[str | None] = mapped_column(Text, nullable=True)

    action: Mapped[str] = mapped_column(Text, nullable=False)
    reason_payload: Mapped[list] = mapped_column(JSON, nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False, default="open")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
