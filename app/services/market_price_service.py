import random
from datetime import datetime, timezone


class MarketPriceService:
    def estimate_from_category(self, opportunity: dict) -> dict:
        base = 50

        if opportunity["category_total_items"]:
            scale = min(opportunity["category_total_items"] / 10000, 5)
            base = base + (scale * 20)

        return {
            "avg_price": round(base, 2),
            "min_price": round(base * 0.6, 2),
            "max_price": round(base * 1.5, 2),
            "sample_size": random.randint(10, 50),
            "source": "heuristic_v1",
            "captured_at": datetime.now(timezone.utc),
        }
