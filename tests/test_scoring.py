from datetime import datetime, timezone

from app.scoring.opportunity import ItemContext, score_item


def test_score_item_returns_bounded_scores() -> None:
    result = score_item(
        ItemContext(
            item_id='MLB123',
            captured_at=datetime.now(timezone.utc),
            trend_hits_7d=7,
            bestseller_hits_7d=3,
            query_presence_24h=7,
            query_presence_7d=14,
            avg_search_position_24h=3,
            avg_search_position_7d=7,
            competitor_cluster_size=5,
            latest_rating_average=4.7,
            required_attr_fill_rate=0.95,
        )
    )
    assert 0 <= result.final_score <= 1
    assert result.demand_score > 0
    assert result.quality_score > 0
