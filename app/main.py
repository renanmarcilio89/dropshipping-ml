import json
from datetime import datetime, timezone

import typer
from sqlalchemy import text

from app.clients.mercadolivre_client import MercadoLivreClient
from app.core.logging import configure_logging
from app.core.settings import get_settings
from app.db.session import SessionLocal, engine
from app.jobs.enrich_items import EnrichItemsJob
from app.jobs.search_marketplace import SearchMarketplaceJob
from app.jobs.sync_trends import SyncTrendsJob
from app.repositories.search_repository import SearchRepository
from app.scoring.opportunity import ItemContext, score_item
from app.services.alert_service import AlertService
from app.services.item_service import ItemService
from app.services.search_service import SearchService

app = typer.Typer(help='CLI do pipeline Mercado Livre.')
settings = get_settings()
configure_logging(settings.log_level)


@app.command()
def health() -> None:
    with engine.connect() as connection:
        connection.execute(text('SELECT 1'))
    typer.echo('ok')


@app.command('sync-trends')
def sync_trends(site_id: str = settings.meli_site_id) -> None:
    db = SessionLocal()
    client = MercadoLivreClient(settings)
    try:
        job = SyncTrendsJob(SearchService(client), SearchRepository(db))
        typer.echo(json.dumps(job.run(site_id), ensure_ascii=False, indent=2))
    finally:
        client.close()
        db.close()


@app.command('search-marketplace')
def search_marketplace(query: str, site_id: str = settings.meli_site_id, offset: int = 0) -> None:
    db = SessionLocal()
    client = MercadoLivreClient(settings)
    try:
        job = SearchMarketplaceJob(SearchService(client), SearchRepository(db))
        typer.echo(json.dumps(job.run(site_id=site_id, query=query, offset=offset), ensure_ascii=False, indent=2))
    finally:
        client.close()
        db.close()


@app.command('enrich-items')
def enrich_items(item_ids: list[str], site_id: str = settings.meli_site_id) -> None:
    db = SessionLocal()
    client = MercadoLivreClient(settings)
    try:
        job = EnrichItemsJob(ItemService(client), SearchRepository(db))
        typer.echo(json.dumps(job.run(site_id=site_id, item_ids=item_ids), ensure_ascii=False, indent=2))
    finally:
        client.close()
        db.close()


@app.command('score-demo')
def score_demo(item_id: str = 'MLB-DEMO') -> None:
    breakdown = score_item(
        ItemContext(
            item_id=item_id,
            captured_at=datetime.now(timezone.utc),
            trend_hits_7d=4,
            bestseller_hits_7d=2,
            query_presence_24h=5,
            query_presence_7d=12,
            avg_search_position_24h=8,
            avg_search_position_7d=12,
            competitor_cluster_size=7,
            latest_rating_average=4.5,
            required_attr_fill_rate=0.9,
            category_logistic_risk='medium',
        )
    )
    alerts = AlertService().build_alerts(breakdown)
    typer.echo(
        json.dumps(
            {'breakdown': breakdown.model_dump(mode='json'), 'alerts': alerts},
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == '__main__':
    app()
