from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Numeric, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class TrendSnapshot(Base):
    __tablename__ = "trend_snapshot"

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

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    source_term: Mapped[str] = mapped_column(Text, nullable=False)
    normalized_term: Mapped[str] = mapped_column(Text, nullable=False)
    candidate_type: Mapped[str] = mapped_column(Text, nullable=False, default="product_term")
    canonical_name: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False, default="pending_enrichment")
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
