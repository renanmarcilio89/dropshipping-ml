from datetime import datetime

from sqlalchemy import JSON, DateTime, Index, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class ApiPayload(Base):
    __tablename__ = "api_payload"
    __table_args__ = (
        UniqueConstraint("payload_hash", name="uq_api_payload_payload_hash"),
        Index("ix_api_payload_captured_at", "captured_at"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    source_name: Mapped[str] = mapped_column(Text, nullable=False)
    site_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    endpoint: Mapped[str] = mapped_column(Text, nullable=False)
    request_params: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    payload: Mapped[dict | list] = mapped_column(JSON, nullable=False)
    payload_hash: Mapped[str] = mapped_column(Text, nullable=False)
    captured_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
