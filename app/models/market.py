from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, Numeric, Text, UniqueConstraint, func
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
