import json
from datetime import datetime, timezone

import typer
from sqlalchemy import text

from app.clients.meli_api_client import MeliApiClient
from app.clients.mercadolivre_client import MercadoLivreClient
from app.core.logging import configure_logging
from app.core.settings import get_settings
from app.db.session import SessionLocal, engine
from app.jobs.enrich_items import EnrichItemsJob
from app.jobs.search_marketplace import SearchMarketplaceJob
from app.jobs.sync_trends import SyncTrendsJob
from app.repositories.meli_credentials import MeliCredentialRepository
from app.repositories.search_repository import SearchRepository
from app.scoring.opportunity import ItemContext, score_item
from app.services.alert_service import AlertService
from app.services.item_service import ItemService
from app.services.meli_auth_service import MeliAuthService
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
    client = MercadoLivreClient(settings, db)
    try:
        job = SyncTrendsJob(SearchService(client), SearchRepository(db))
        typer.echo(json.dumps(job.run(site_id), ensure_ascii=False, indent=2))
    finally:
        client.close()
        db.close()


@app.command('search-marketplace')
def search_marketplace(query: str, site_id: str = settings.meli_site_id, offset: int = 0) -> None:
    db = SessionLocal()
    client = MercadoLivreClient(settings, db)
    try:
        job = SearchMarketplaceJob(SearchService(client), SearchRepository(db))
        typer.echo(json.dumps(job.run(site_id=site_id, query=query, offset=offset), ensure_ascii=False, indent=2))
    finally:
        client.close()
        db.close()


@app.command('enrich-items')
def enrich_items(item_ids: list[str], site_id: str = settings.meli_site_id) -> None:
    db = SessionLocal()
    client = MercadoLivreClient(settings, db)
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


@app.command('auth-bootstrap')
def auth_bootstrap(code: str) -> None:
    """
    Troca o authorization code por tokens e salva no banco.
    """
    auth_service = MeliAuthService()
    token_data = auth_service.exchange_code_for_token(code)
    current_user = auth_service.get_current_user(token_data.access_token)
    expires_at = auth_service.calculate_expires_at(token_data.expires_in)

    db = SessionLocal()
    try:
        repo = MeliCredentialRepository(db)
        stored = repo.upsert_tokens(
            token_data=token_data,
            expires_at=expires_at,
            nickname=current_user.nickname,
        )
        typer.echo(
            f'Tokens salvos com sucesso para user_id={stored.user_id} nickname={stored.nickname}'
        )
    finally:
        db.close()


@app.command('auth-current-user')
def auth_current_user() -> None:
    """
    Lê o usuário atual usando token válido, com refresh automático.
    """
    db = SessionLocal()
    try:
        client = MeliApiClient(db)
        payload = client.get('/users/me')
        typer.echo(json.dumps(payload, ensure_ascii=False, indent=2))
    finally:
        db.close()


@app.command('auth-refresh')
def auth_refresh() -> None:
    """
    Força um refresh do token armazenado.
    """
    db = SessionLocal()
    try:
        client = MeliApiClient(db)
        token = client._refresh_and_get_access_token()
        typer.echo(f'Novo access token obtido com sucesso: {token[:16]}...')
    finally:
        db.close()


if __name__ == '__main__':
    app()
