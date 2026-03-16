from dataclasses import dataclass
from datetime import datetime

from app.core.constants import DEFAULT_SCORE_VERSION
from app.schemas.common import OpportunityBreakdown


@dataclass(slots=True)
class ItemContext:
    item_id: str
    captured_at: datetime
    trend_hits_7d: int = 0
    bestseller_hits_7d: int = 0
    query_presence_24h: int = 0
    query_presence_7d: int = 0
    avg_search_position_24h: float | None = None
    avg_search_position_7d: float | None = None
    competitor_cluster_size: int = 0
    catalog_listing_flag: bool = False
    latest_rating_average: float | None = None
    required_attr_fill_rate: float = 0.0
    category_logistic_risk: str = 'medium'
    is_fragile: bool = False
    requires_size_or_fit_precision: bool = False
    low_rating_with_high_volume: bool = False


def _clamp(value: float) -> float:
    return max(0.0, min(value, 1.0))


def _inverse_position(value: float | None, max_position: float = 100.0) -> float:
    if value is None:
        return 0.0
    return _clamp((max_position - min(value, max_position)) / max_position)


def demand_score(ctx: ItemContext) -> float:
    trend_component = min(ctx.trend_hits_7d / 7.0, 1.0)
    bestseller_component = min(ctx.bestseller_hits_7d / 7.0, 1.0)
    query_component = min(ctx.query_presence_7d / 20.0, 1.0)
    return _clamp(0.45 * trend_component + 0.35 * bestseller_component + 0.20 * query_component)


def traction_score(ctx: ItemContext) -> float:
    pos24 = _inverse_position(ctx.avg_search_position_24h)
    pos7 = _inverse_position(ctx.avg_search_position_7d)
    ubiquity = min(ctx.query_presence_24h / 10.0, 1.0)
    return _clamp(0.40 * pos24 + 0.35 * pos7 + 0.25 * ubiquity)


def competition_score(ctx: ItemContext) -> float:
    cluster_penalty = min(ctx.competitor_cluster_size / 25.0, 1.0)
    catalog_penalty = 1.0 if ctx.catalog_listing_flag else 0.3
    return _clamp(1.0 - (0.70 * cluster_penalty + 0.30 * catalog_penalty))


def quality_score(ctx: ItemContext) -> float:
    rating = 0.5 if ctx.latest_rating_average is None else min(ctx.latest_rating_average / 5.0, 1.0)
    attr_fill = min(ctx.required_attr_fill_rate, 1.0)
    return _clamp(0.65 * rating + 0.35 * attr_fill)


def ops_risk_score(ctx: ItemContext) -> float:
    risk = 0.0
    if ctx.category_logistic_risk == 'high':
        risk += 0.40
    elif ctx.category_logistic_risk == 'medium':
        risk += 0.20
    if ctx.is_fragile:
        risk += 0.20
    if ctx.requires_size_or_fit_precision:
        risk += 0.20
    if ctx.low_rating_with_high_volume:
        risk += 0.20
    return _clamp(risk)


def final_score(demand: float, traction: float, competition: float, quality: float, ops_risk: float) -> float:
    return _clamp(0.30 * demand + 0.25 * traction + 0.20 * competition + 0.15 * quality - 0.10 * ops_risk)


def score_item(ctx: ItemContext, score_version: str = DEFAULT_SCORE_VERSION) -> OpportunityBreakdown:
    demand = demand_score(ctx)
    traction = traction_score(ctx)
    competition = competition_score(ctx)
    quality = quality_score(ctx)
    ops_risk = ops_risk_score(ctx)
    final = final_score(demand, traction, competition, quality, ops_risk)
    return OpportunityBreakdown(
        entity_type='item',
        entity_id=ctx.item_id,
        captured_at=ctx.captured_at,
        demand_score=demand,
        traction_score=traction,
        competition_score=competition,
        quality_score=quality,
        ops_risk_score=ops_risk,
        final_score=final,
        score_version=score_version,
    )
