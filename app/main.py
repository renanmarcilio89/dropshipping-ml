import json
from datetime import datetime, timezone

import typer
from sqlalchemy import text

from app.clients.meli_api_client import MeliApiClient
from app.clients.mercadolivre_client import MercadoLivreClient
from app.core.logging import configure_logging
from app.core.settings import get_settings
from app.db.session import SessionLocal, engine
from app.jobs.build_candidates import BuildCandidatesJob
from app.jobs.enrich_candidates import EnrichCandidatesJob
from app.jobs.sync_trends import SyncTrendsJob
from app.jobs.qualify_candidates import QualifyCandidatesJob
from app.repositories.candidate_market_snapshot_repository import CandidateMarketSnapshotRepository
from app.repositories.candidate_repository import CandidateRepository
from app.repositories.meli_credentials import MeliCredentialRepository
from app.repositories.raw_payload_repository import RawPayloadRepository
from app.repositories.trend_repository import TrendRepository
from app.services.candidate_enrichment_service import CandidateEnrichmentService
from app.services.candidate_qualification_service import CandidateQualificationService
from app.services.candidate_service import CandidateService
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
        job = SyncTrendsJob(
            SearchService(client),
            TrendRepository(db),
            RawPayloadRepository(db),
        )
        typer.echo(json.dumps(job.run(site_id), ensure_ascii=False, indent=2))
    finally:
        client.close()
        db.close()


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


@app.command("build-candidates")
def build_candidates(trend_limit: int = 100) -> None:
    db = SessionLocal()
    try:
        job = BuildCandidatesJob(
            trend_repository=TrendRepository(db),
            candidate_repository=CandidateRepository(db),
            candidate_service=CandidateService(),
        )
        typer.echo(json.dumps(job.run(trend_limit=trend_limit), ensure_ascii=False, indent=2))
    finally:
        db.close()


@app.command("qualify-candidates")
def qualify_candidates(limit: int = 100) -> None:
    db = SessionLocal()
    try:
        job = QualifyCandidatesJob(
            candidate_repository=CandidateRepository(db),
            qualification_service=CandidateQualificationService(),
        )
        typer.echo(json.dumps(job.run(limit=limit), ensure_ascii=False, indent=2))
    finally:
        db.close()


@app.command("enrich-candidates")
def enrich_candidates(
    limit: int = 20,
    search_limit: int = 20,
    site_id: str = settings.meli_site_id,
) -> None:
    db = SessionLocal()
    client = MercadoLivreClient(settings, db)
    try:
        job = EnrichCandidatesJob(
            candidate_repository=CandidateRepository(db),
            snapshot_repository=CandidateMarketSnapshotRepository(db),
            raw_payload_repository=RawPayloadRepository(db),
            enrichment_service=CandidateEnrichmentService(client),
        )
        typer.echo(
            json.dumps(
                job.run(site_id=site_id, limit=limit, search_limit=search_limit),
                ensure_ascii=False,
                indent=2,
            )
        )
    finally:
        client.close()
        db.close()


if __name__ == '__main__':
    app()
