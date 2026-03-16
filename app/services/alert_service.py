from app.schemas.common import OpportunityBreakdown


class AlertService:
    def build_alerts(self, breakdown: OpportunityBreakdown) -> list[str]:
        alerts: list[str] = []
        if breakdown.demand_score >= 0.80 and breakdown.competition_score >= 0.65:
            alerts.append('LOW_COMPETITION_HIGH_DEMAND')
        if breakdown.traction_score >= 0.85 and breakdown.final_score >= 0.75:
            alerts.append('SEARCH_BREAKOUT')
        if breakdown.quality_score <= 0.35 and breakdown.demand_score >= 0.70:
            alerts.append('QUALITY_RISK')
        if breakdown.ops_risk_score >= 0.70 and breakdown.final_score >= 0.70:
            alerts.append('OPS_RISK')
        return alerts
