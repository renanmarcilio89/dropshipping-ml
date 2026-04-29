import json

import typer
from sqlalchemy import text

from app.clients.meli_api_client import MeliApiClient
from app.clients.mercadolivre_client import MercadoLivreClient
from app.core.logging import configure_logging
from app.core.settings import get_settings
from app.db.session import SessionLocal, engine
from app.jobs.alert_opportunities import AlertOpportunitiesJob
from app.jobs.analyze_commercial_opportunities import AnalyzeCommercialOpportunitiesJob
from app.jobs.analyze_market_reality import AnalyzeMarketRealityJob
from app.jobs.build_candidates import BuildCandidatesJob
from app.jobs.enrich_candidates import EnrichCandidatesJob
from app.jobs.list_alerts import ListAlertsJob
from app.jobs.list_commercial_analyses import ListCommercialAnalysesJob
from app.jobs.list_investment_priorities import ListInvestmentPrioritiesJob
from app.jobs.list_market_reality import ListMarketRealityJob
from app.jobs.qualify_candidates import QualifyCandidatesJob
from app.jobs.rank_opportunities import RankOpportunitiesJob
from app.jobs.score_candidates import ScoreCandidatesJob
from app.jobs.sync_trends import SyncTrendsJob
from app.presenters.output_presenter import OutputPresenter
from app.repositories.candidate_market_snapshot_repository import (
    CandidateMarketSnapshotRepository,
)
from app.repositories.candidate_repository import CandidateRepository
from app.repositories.commercial_opportunity_analysis_repository import (
    CommercialOpportunityAnalysisRepository,
)
from app.repositories.investment_priority_repository import InvestmentPriorityRepository
from app.repositories.market_reality_analysis_repository import (
    MarketRealityAnalysisRepository,
)
from app.repositories.meli_credentials import MeliCredentialRepository
from app.repositories.opportunity_alert_query_repository import (
    OpportunityAlertQueryRepository,
)
from app.repositories.opportunity_alert_repository import OpportunityAlertRepository
from app.repositories.opportunity_ranking_repository import OpportunityRankingRepository
from app.repositories.opportunity_score_repository import OpportunityScoreRepository
from app.repositories.raw_payload_repository import RawPayloadRepository
from app.repositories.trend_repository import TrendRepository
from app.services.candidate_enrichment_service import CandidateEnrichmentService
from app.services.candidate_qualification_service import CandidateQualificationService
from app.services.candidate_service import CandidateService
from app.services.commercial_opportunity_query_service import (
    CommercialOpportunityQueryService,
)
from app.services.commercial_opportunity_service import CommercialOpportunityService
from app.services.investment_priority_service import InvestmentPriorityService
from app.services.market_reality_query_service import MarketRealityQueryService
from app.services.market_reality_service import MarketRealityService
from app.services.meli_auth_service import MeliAuthService
from app.services.opportunity_alert_query_service import OpportunityAlertQueryService
from app.services.opportunity_alert_service import OpportunityAlertService
from app.services.opportunity_ranking_service import OpportunityRankingService
from app.services.opportunity_scoring_service import OpportunityScoringService
from app.services.search_service import SearchService

app = typer.Typer(help="CLI do pipeline Mercado Livre.")
settings = get_settings()
configure_logging(settings.log_level)


def echo_json(payload: object, *, language: str = "en") -> None:
    presented_payload = OutputPresenter.present(payload, language=language)
    typer.echo(
        json.dumps(
            presented_payload,
            ensure_ascii=False,
            indent=2,
        )
    )


@app.command()
def health() -> None:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    typer.echo("ok")


@app.command("sync-trends")
def sync_trends(
    site_id: str = settings.meli_site_id,
    language: str = typer.Option(
        "en",
        help="Output language: en or pt-BR.",
    ),
) -> None:
    db = SessionLocal()
    client = MercadoLivreClient(settings, db)
    try:
        job = SyncTrendsJob(
            SearchService(client),
            TrendRepository(db),
            RawPayloadRepository(db),
        )
        result = job.run(site_id)
        echo_json(result, language=language)
    finally:
        client.close()
        db.close()


@app.command("auth-bootstrap")
def auth_bootstrap(code: str) -> None:
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
        db.commit()
        typer.echo(
            f"Tokens salvos com sucesso para user_id={stored.user_id} nickname={stored.nickname}"
        )
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@app.command("auth-current-user")
def auth_current_user(
    language: str = typer.Option(
        "en",
        help="Output language: en or pt-BR.",
    ),
) -> None:
    db = SessionLocal()
    try:
        client = MeliApiClient(db)
        payload = client.get("/users/me")
        echo_json(payload, language=language)
    finally:
        db.close()


@app.command("auth-refresh")
def auth_refresh() -> None:
    db = SessionLocal()
    try:
        client = MeliApiClient(db)
        token = client._refresh_and_get_access_token()
        typer.echo(f"Novo access token obtido com sucesso: {token[:16]}...")
    finally:
        db.close()


@app.command("build-candidates")
def build_candidates(
    trend_limit: int = 100,
    language: str = typer.Option(
        "en",
        help="Output language: en or pt-BR.",
    ),
) -> None:
    db = SessionLocal()
    try:
        job = BuildCandidatesJob(
            trend_repository=TrendRepository(db),
            candidate_repository=CandidateRepository(db),
            candidate_service=CandidateService(),
        )
        result = job.run(trend_limit=trend_limit)
        db.commit()
        echo_json(result, language=language)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@app.command("qualify-candidates")
def qualify_candidates(
    limit: int = 100,
    language: str = typer.Option(
        "en",
        help="Output language: en or pt-BR.",
    ),
) -> None:
    db = SessionLocal()
    try:
        job = QualifyCandidatesJob(
            candidate_repository=CandidateRepository(db),
            qualification_service=CandidateQualificationService(),
        )
        result = job.run(limit=limit)
        db.commit()
        echo_json(result, language=language)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@app.command("enrich-candidates")
def enrich_candidates(
    limit: int = 20,
    site_id: str = settings.meli_site_id,
    force: bool = typer.Option(
        False,
        "--force",
        help="Reprocess candidates already enriched or with enrichment failure.",
    ),
    language: str = typer.Option(
        "en",
        help="Output language: en or pt-BR.",
    ),
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
        result = job.run(site_id=site_id, limit=limit, force=force)
        db.commit()
        echo_json(result, language=language)
    except Exception:
        db.rollback()
        raise
    finally:
        client.close()
        db.close()


@app.command("score-candidates")
def score_candidates(
    limit: int = 100,
    force: bool = typer.Option(
        False,
        "--force",
        help="Recalculates the score of candidates who already have an enrichment snapshot.",
    ),
    language: str = typer.Option(
        "en",
        help="Output language: en or pt-BR.",
    ),
) -> None:
    db = SessionLocal()
    try:
        job = ScoreCandidatesJob(
            candidate_repository=CandidateRepository(db),
            snapshot_repository=CandidateMarketSnapshotRepository(db),
            opportunity_score_repository=OpportunityScoreRepository(db),
            scoring_service=OpportunityScoringService(),
        )
        result = job.run(limit=limit, force=force)
        db.commit()
        echo_json(result, language=language)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@app.command("rank-opportunities")
def rank_opportunities(
    limit: int = 20,
    min_final_score: float | None = typer.Option(
        None,
        help="Retorna apenas oportunidades com final_score maior ou igual a este valor.",
    ),
    confidence_level: str | None = typer.Option(
        None,
        help="Filtra por nível de confiança: high, medium, low ou none.",
    ),
    listing_allowed: bool | None = typer.Option(
        None,
        help="Filtra por categorias com listing_allowed true/false.",
    ),
    max_category_total_items: int | None = typer.Option(
        None,
        help="Filtra categorias com até este total de itens.",
    ),
    language: str = typer.Option(
        "en",
        help="Output language: en or pt-BR.",
    ),
) -> None:
    db = SessionLocal()
    try:
        job = RankOpportunitiesJob(
            ranking_repository=OpportunityRankingRepository(db),
            ranking_service=OpportunityRankingService(),
        )
        result = job.run(
            limit=limit,
            min_final_score=min_final_score,
            confidence_level=confidence_level,
            listing_allowed=listing_allowed,
            max_category_total_items=max_category_total_items,
        )
        echo_json(result, language=language)
    finally:
        db.close()


@app.command("alert-opportunities")
def alert_opportunities(
    limit: int = 50,
    language: str = typer.Option(
        "en",
        help="Output language: en or pt-BR.",
    ),
) -> None:
    db = SessionLocal()
    try:
        job = AlertOpportunitiesJob(
            ranking_repository=OpportunityRankingRepository(db),
            ranking_service=OpportunityRankingService(),
            alert_service=OpportunityAlertService(),
            alert_repository=OpportunityAlertRepository(db),
        )

        result = job.run(limit=limit)
        db.commit()
        echo_json(result, language=language)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@app.command("list-alerts")
def list_alerts(
    limit: int = 50,
    status: str | None = typer.Option(
        None,
        help="Filtra por status: open, dismissed ou acted.",
    ),
    min_final_score: float | None = typer.Option(
        None,
        help="Retorna apenas alerts com final_score maior ou igual a este valor.",
    ),
    confidence_level: str | None = typer.Option(
        None,
        help="Filtra por confidence_level: high, medium, low ou none.",
    ),
    language: str = typer.Option(
        "en",
        help="Output language: en or pt-BR.",
    ),
) -> None:
    db = SessionLocal()
    try:
        job = ListAlertsJob(
            alert_query_repository=OpportunityAlertQueryRepository(db),
            alert_query_service=OpportunityAlertQueryService(),
        )
        result = job.run(
            limit=limit,
            status=status,
            min_final_score=min_final_score,
            confidence_level=confidence_level,
        )
        echo_json(result, language=language)
    finally:
        db.close()


@app.command("commercial-opportunities")
def commercial_opportunities(
    limit: int = 20,
    language: str = typer.Option(
        "en",
        help="Output language: en or pt-BR.",
    ),
) -> None:
    db = SessionLocal()
    try:
        job = AnalyzeCommercialOpportunitiesJob(
            ranking_repository=OpportunityRankingRepository(db),
            ranking_service=OpportunityRankingService(),
            commercial_service=CommercialOpportunityService(),
            analysis_repository=CommercialOpportunityAnalysisRepository(db),
        )

        result = job.run(limit=limit)
        db.commit()
        echo_json(result, language=language)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@app.command("list-commercial-analyses")
def list_commercial_analyses(
    limit: int = 20,
    commercial_decision: str | None = typer.Option(
        None,
        help="Filtra por decisão: dropshipping_candidate, affiliate_candidate, research_needed ou avoid.",
    ),
    risk_level: str | None = typer.Option(
        None,
        help="Filtra por risco: low, medium ou high.",
    ),
    min_commercial_score: float | None = typer.Option(
        None,
        help="Retorna apenas análises com commercial_score maior ou igual a este valor.",
    ),
    language: str = typer.Option(
        "en",
        help="Output language: en or pt-BR.",
    ),
) -> None:
    db = SessionLocal()
    try:
        job = ListCommercialAnalysesJob(
            analysis_repository=CommercialOpportunityAnalysisRepository(db),
            query_service=CommercialOpportunityQueryService(),
        )

        result = job.run(
            limit=limit,
            commercial_decision=commercial_decision,
            risk_level=risk_level,
            min_commercial_score=min_commercial_score,
        )
        echo_json(result, language=language)
    finally:
        db.close()


@app.command("market-reality")
def market_reality(
    candidate_id: int = typer.Option(..., help="Candidate id."),
    sale_price: float = typer.Option(..., help="Expected sale price."),
    supplier_cost: float = typer.Option(..., help="Supplier product cost."),
    shipping_cost: float = typer.Option(..., help="Expected shipping cost."),
    marketplace_fee_rate: float = typer.Option(
        ...,
        help="Marketplace fee rate. Example: 0.16 for 16 percent.",
    ),
    ads_cost_rate: float = typer.Option(
        0.0,
        help="Ads cost rate. Example: 0.08 for 8 percent.",
    ),
    language: str = typer.Option(
        "en",
        help="Output language: en or pt-BR.",
    ),
) -> None:
    db = SessionLocal()
    try:
        job = AnalyzeMarketRealityJob(
            market_reality_service=MarketRealityService(),
            analysis_repository=MarketRealityAnalysisRepository(db),
        )

        result = job.run(
            candidate_id=candidate_id,
            sale_price=sale_price,
            supplier_cost=supplier_cost,
            shipping_cost=shipping_cost,
            marketplace_fee_rate=marketplace_fee_rate,
            ads_cost_rate=ads_cost_rate,
        )
        db.commit()
        echo_json(result, language=language)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@app.command("list-market-reality")
def list_market_reality(
    limit: int = 20,
    candidate_id: int | None = typer.Option(
        None,
        help="Candidate id.",
    ),
    viability_level: str | None = typer.Option(
        None,
        help="Filter by viability level: strong, viable, thin, weak or unprofitable.",
    ),
    min_estimated_margin: float | None = typer.Option(
        None,
        help="Return only analyses with estimated_margin greater than or equal to this value.",
    ),
    min_estimated_profit: float | None = typer.Option(
        None,
        help="Return only analyses with estimated_profit greater than or equal to this value.",
    ),
    language: str = typer.Option(
        "en",
        help="Output language: en or pt-BR.",
    ),
) -> None:
    db = SessionLocal()
    try:
        job = ListMarketRealityJob(
            analysis_repository=MarketRealityAnalysisRepository(db),
            query_service=MarketRealityQueryService(),
        )

        result = job.run(
            limit=limit,
            candidate_id=candidate_id,
            viability_level=viability_level,
            min_estimated_margin=min_estimated_margin,
            min_estimated_profit=min_estimated_profit,
        )
        echo_json(result, language=language)
    finally:
        db.close()


@app.command("investment-priorities")
def investment_priorities(
    limit: int = 20,
    min_final_score: float | None = typer.Option(
        None,
        help="Return only priorities with final_score greater than or equal to this value.",
    ),
    min_commercial_score: float | None = typer.Option(
        None,
        help="Return only priorities with commercial_score greater than or equal to this value.",
    ),
    min_estimated_margin: float | None = typer.Option(
        None,
        help="Return only priorities with estimated_margin greater than or equal to this value.",
    ),
    commercial_decision: str | None = typer.Option(
        None,
        help="Filter by commercial decision.",
    ),
    viability_level: str | None = typer.Option(
        None,
        help="Filter by viability level.",
    ),
    language: str = typer.Option(
        "en",
        help="Output language: en or pt-BR.",
    ),
) -> None:
    db = SessionLocal()
    try:
        job = ListInvestmentPrioritiesJob(
            priority_repository=InvestmentPriorityRepository(db),
            priority_service=InvestmentPriorityService(),
            commercial_query_service=CommercialOpportunityQueryService(),
            market_reality_query_service=MarketRealityQueryService(),
        )

        result = job.run(
            limit=limit,
            min_final_score=min_final_score,
            min_commercial_score=min_commercial_score,
            min_estimated_margin=min_estimated_margin,
            commercial_decision=commercial_decision,
            viability_level=viability_level,
        )
        echo_json(result, language=language)
    finally:
        db.close()


if __name__ == "__main__":
    app()
