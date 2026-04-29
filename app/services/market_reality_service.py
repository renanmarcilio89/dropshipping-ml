from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MarketRealityInput:
    candidate_id: int
    sale_price: float
    supplier_cost: float
    shipping_cost: float
    marketplace_fee_rate: float
    ads_cost_rate: float = 0.0


@dataclass(frozen=True)
class MarketRealityResult:
    candidate_id: int
    sale_price: float
    supplier_cost: float
    shipping_cost: float
    marketplace_fee: float
    ads_cost: float
    total_cost: float
    estimated_profit: float
    estimated_margin: float
    estimated_margin_percent: float
    break_even_price: float
    viability_level: str
    recommendation: str


class MarketRealityService:
    def analyze(self, data: MarketRealityInput) -> MarketRealityResult:
        marketplace_fee = round(data.sale_price * data.marketplace_fee_rate, 2)
        ads_cost = round(data.sale_price * data.ads_cost_rate, 2)
        total_cost = round(
            data.supplier_cost + data.shipping_cost + marketplace_fee + ads_cost,
            2,
        )
        estimated_profit = round(data.sale_price - total_cost, 2)
        estimated_margin = self._margin(estimated_profit, data.sale_price)
        estimated_margin_percent = round(estimated_margin * 100, 2)
        break_even_price = self._break_even_price(
            supplier_cost=data.supplier_cost,
            shipping_cost=data.shipping_cost,
            marketplace_fee_rate=data.marketplace_fee_rate,
            ads_cost_rate=data.ads_cost_rate,
        )
        viability_level = self._viability_level(estimated_margin, estimated_profit)
        recommendation = self._recommendation(viability_level)

        return MarketRealityResult(
            candidate_id=data.candidate_id,
            sale_price=round(data.sale_price, 2),
            supplier_cost=round(data.supplier_cost, 2),
            shipping_cost=round(data.shipping_cost, 2),
            marketplace_fee=marketplace_fee,
            ads_cost=ads_cost,
            total_cost=total_cost,
            estimated_profit=estimated_profit,
            estimated_margin=estimated_margin,
            estimated_margin_percent=estimated_margin_percent,
            break_even_price=break_even_price,
            viability_level=viability_level,
            recommendation=recommendation,
        )

    @staticmethod
    def _margin(profit: float, sale_price: float) -> float:
        if sale_price <= 0:
            return 0.0
        return round(profit / sale_price, 4)

    @staticmethod
    def _break_even_price(
        *,
        supplier_cost: float,
        shipping_cost: float,
        marketplace_fee_rate: float,
        ads_cost_rate: float,
    ) -> float:
        variable_rate = marketplace_fee_rate + ads_cost_rate
        denominator = 1.0 - variable_rate

        if denominator <= 0:
            return 0.0

        return round((supplier_cost + shipping_cost) / denominator, 2)

    @staticmethod
    def _viability_level(margin: float, profit: float) -> str:
        if profit <= 0:
            return "unprofitable"
        if margin >= 0.30:
            return "strong"
        if margin >= 0.18:
            return "viable"
        if margin >= 0.10:
            return "thin"
        return "weak"

    @staticmethod
    def _recommendation(viability_level: str) -> str:
        recommendations = {
            "strong": "Proceed to validate demand, supplier reliability, and fulfillment constraints.",
            "viable": "Proceed with caution and validate acquisition costs before scaling.",
            "thin": "Only proceed if demand is strong or if costs can be reduced.",
            "weak": "Do not prioritize unless supplier cost, fees, or shipping can improve.",
            "unprofitable": "Avoid this scenario because estimated profit is negative or zero.",
        }
        return recommendations[viability_level]
