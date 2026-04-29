from app.models.market import MarketRealityAnalysis


class MarketRealityQueryService:
    @staticmethod
    def build_output(analyses: list[MarketRealityAnalysis]) -> list[dict]:
        return [
            {
                "id": analysis.id,
                "candidate_id": analysis.candidate_id,
                "sale_price": float(analysis.sale_price),
                "supplier_cost": float(analysis.supplier_cost),
                "shipping_cost": float(analysis.shipping_cost),
                "marketplace_fee_rate": float(analysis.marketplace_fee_rate),
                "ads_cost_rate": float(analysis.ads_cost_rate),
                "marketplace_fee": float(analysis.marketplace_fee),
                "ads_cost": float(analysis.ads_cost),
                "total_cost": float(analysis.total_cost),
                "estimated_profit": float(analysis.estimated_profit),
                "estimated_margin": float(analysis.estimated_margin),
                "estimated_margin_percent": round(float(analysis.estimated_margin) * 100, 2),
                "break_even_price": float(analysis.break_even_price),
                "viability_level": analysis.viability_level,
                "recommendation": analysis.recommendation,
                "analysis_version": analysis.analysis_version,
                "created_at": analysis.created_at.isoformat()
                if analysis.created_at
                else None,
            }
            for analysis in analyses
        ]

    @staticmethod
    def normalize_viability_level(value: str | None) -> str | None:
        if value is None:
            return None

        normalized = value.strip().lower()
        allowed = {"strong", "viable", "thin", "weak", "unprofitable"}

        if normalized in allowed:
            return normalized

        raise ValueError(
            "viability_level invalido. Use: strong, viable, thin, weak ou unprofitable."
        )
