from app.models.market import MarketRealityAnalysis


class MarketRealityAnalysisRepository:
    def __init__(self, session) -> None:
        self.session = session

    def create(self, analysis: dict, *, analysis_version: str) -> MarketRealityAnalysis:
        record = MarketRealityAnalysis(
            candidate_id=analysis["candidate_id"],
            sale_price=analysis["sale_price"],
            supplier_cost=analysis["supplier_cost"],
            shipping_cost=analysis["shipping_cost"],
            marketplace_fee_rate=analysis["marketplace_fee_rate"],
            ads_cost_rate=analysis["ads_cost_rate"],
            marketplace_fee=analysis["marketplace_fee"],
            ads_cost=analysis["ads_cost"],
            total_cost=analysis["total_cost"],
            estimated_profit=analysis["estimated_profit"],
            estimated_margin=analysis["estimated_margin"],
            break_even_price=analysis["break_even_price"],
            viability_level=analysis["viability_level"],
            recommendation=analysis["recommendation"],
            analysis_version=analysis_version,
        )

        self.session.add(record)
        return record
