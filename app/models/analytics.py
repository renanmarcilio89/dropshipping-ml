from datetime import datetime

from sqlalchemy import DateTime, Integer, JSON, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class OpportunityScore(Base):
    __tablename__ = 'opportunity_score'
    __table_args__ = {'schema': 'ml_analytics'}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    entity_type: Mapped[str] = mapped_column(String, nullable=False)
    entity_id: Mapped[str] = mapped_column(String, nullable=False)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    final_score: Mapped[float] = mapped_column(Numeric(8, 4), nullable=False)
    demand_score: Mapped[float] = mapped_column(Numeric(8, 4), nullable=False)
    traction_score: Mapped[float] = mapped_column(Numeric(8, 4), nullable=False)
    competition_score: Mapped[float] = mapped_column(Numeric(8, 4), nullable=False)
    quality_score: Mapped[float] = mapped_column(Numeric(8, 4), nullable=False)
    ops_risk_score: Mapped[float] = mapped_column(Numeric(8, 4), nullable=False)
    score_version: Mapped[str] = mapped_column(String, nullable=False)


class AlertEvent(Base):
    __tablename__ = 'alert_event'
    __table_args__ = {'schema': 'ml_analytics'}

    alert_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    alert_type: Mapped[str] = mapped_column(String, nullable=False)
    severity: Mapped[str] = mapped_column(String, nullable=False)
    entity_type: Mapped[str] = mapped_column(String, nullable=False)
    entity_id: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    payload_json: Mapped[dict] = mapped_column(JSON, nullable=False)
    status: Mapped[str] = mapped_column(String, default='open')


class ItemFeatureFact(Base):
    __tablename__ = 'item_feature_fact'
    __table_args__ = {'schema': 'ml_analytics'}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    item_id: Mapped[str] = mapped_column(String, nullable=False)
    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    demand_score: Mapped[float] = mapped_column(Numeric(8, 4), nullable=False)
    traction_score: Mapped[float] = mapped_column(Numeric(8, 4), nullable=False)
    competition_score: Mapped[float] = mapped_column(Numeric(8, 4), nullable=False)
    quality_score: Mapped[float] = mapped_column(Numeric(8, 4), nullable=False)
    ops_risk_score: Mapped[float] = mapped_column(Numeric(8, 4), nullable=False)
    query_presence_24h: Mapped[int | None] = mapped_column(Integer, nullable=True)
    query_presence_7d: Mapped[int | None] = mapped_column(Integer, nullable=True)
    avg_search_position_24h: Mapped[float | None] = mapped_column(Numeric(8, 2), nullable=True)
    avg_search_position_7d: Mapped[float | None] = mapped_column(Numeric(8, 2), nullable=True)
    trend_hits_7d: Mapped[int | None] = mapped_column(Integer, nullable=True)
    bestseller_hits_7d: Mapped[int | None] = mapped_column(Integer, nullable=True)
    competitor_cluster_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    latest_rating_average: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    score_version: Mapped[str] = mapped_column(String, nullable=False)
