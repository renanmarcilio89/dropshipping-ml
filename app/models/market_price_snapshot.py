from datetime import datetime
from sqlalchemy import Text, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class MarketPriceSnapshot(Base):
    __tablename__ = "market_price_snapshot"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidate.id"))

    avg_price: Mapped[float | None] = mapped_column(Numeric(10, 2))
    min_price: Mapped[float | None] = mapped_column(Numeric(10, 2))
    max_price: Mapped[float | None] = mapped_column(Numeric(10, 2))

    sample_size: Mapped[int] = mapped_column()
    source: Mapped[str] = mapped_column(Text)

    captured_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
