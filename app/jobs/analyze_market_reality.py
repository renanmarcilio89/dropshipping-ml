from app.repositories.market_reality_analysis_repository import (
    MarketRealityAnalysisRepository,
)
from app.services.market_reality_service import (
    MarketRealityInput,
    MarketRealityService,
)


class AnalyzeMarketRealityJob:
    ANALYSIS_VERSION = "v1_manual_market_reality"

    def __init__(
        self,
        *,
        market_reality_service: MarketRealityService,
        analysis_repository: MarketRealityAnalysisRepository,
    ) -> None:
        self.market_reality_service = market_reality_service
        self.analysis_repository = analysis_repository

    def run(
        self,
        *,
        candidate_id: int,
        sale_price: float,
        supplier_cost: float,
        shipping_cost: float,
        marketplace_fee_rate: float,
        ads_cost_rate: float = 0.0,
    ) -> dict:
        result = self.market_reality_service.analyze(
            MarketRealityInput(
                candidate_id=candidate_id,
                sale_price=sale_price,
                supplier_cost=supplier_cost,
                shipping_cost=shipping_cost,
                marketplace_fee_rate=marketplace_fee_rate,
                ads_cost_rate=ads_cost_rate,
            )
        )

        analysis = {
            "candidate_id": result.candidate_id,
            "sale_price": result.sale_price,
            "supplier_cost": result.supplier_cost,
            "shipping_cost": result.shipping_cost,
            "marketplace_fee_rate": marketplace_fee_rate,
            "ads_cost_rate": ads_cost_rate,
            "marketplace_fee": result.marketplace_fee,
            "ads_cost": result.ads_cost,
            "total_cost": result.total_cost,
            "estimated_profit": result.estimated_profit,
            "estimated_margin": result.estimated_margin,
            "break_even_price": result.break_even_price,
            "viability_level": result.viability_level,
            "recommendation": result.recommendation,
            "analysis_version": self.ANALYSIS_VERSION,
        }

        self.analysis_repository.create(
            analysis,
            analysis_version=self.ANALYSIS_VERSION,
        )

        return analysis
