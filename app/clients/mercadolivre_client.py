from __future__ import annotations

from typing import Any

import httpx
from sqlalchemy.orm import Session
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from app.clients.meli_api_client import MeliApiClient
from app.core.constants import DEFAULT_LIMIT, MULTIGET_MAX_ITEMS
from app.core.exceptions import ConfigurationError, MeliAPIError
from app.core.settings import Settings


class MercadoLivreClient:
    def __init__(self, settings: Settings, db_session: Session | None = None) -> None:
        self.settings = settings
        self.db_session = db_session
        self.auth_client = MeliApiClient(db_session) if db_session is not None else None

        self._client = httpx.Client(
            base_url=settings.meli_base_url,
            timeout=settings.request_timeout_seconds,
            headers={'Accept': 'application/json'},
        )

    def close(self) -> None:
        self._client.close()

    def _build_headers(self, authenticated: bool = False) -> dict[str, str]:
        headers = {'Accept': 'application/json'}

        if authenticated:
            token = self._get_access_token()
            headers['Authorization'] = f'Bearer {token}'
        elif self.settings.meli_access_token:
            headers['Authorization'] = f'Bearer {self.settings.meli_access_token}'

        return headers

    def _get_access_token(self) -> str:
        if self.auth_client is not None:
            return self.auth_client._get_valid_access_token()

        if self.settings.meli_access_token:
            return self.settings.meli_access_token

        raise ConfigurationError(
            'Nenhum token disponível. Configure MELI_ACCESS_TOKEN ou use credenciais persistidas no banco.'
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(1),
        retry=retry_if_exception_type((httpx.HTTPError, MeliAPIError)),
        reraise=True,
    )
    def _get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
        authenticated: bool = False,
    ) -> dict[str, Any] | list[dict[str, Any]]:
        response = self._client.get(
            path,
            params=params,
            headers=self._build_headers(authenticated=authenticated),
        )

        if response.status_code == 401 and authenticated and self.auth_client is not None:
            token = self.auth_client._refresh_and_get_access_token()
            response = self._client.get(
                path,
                params=params,
                headers={
                    'Accept': 'application/json',
                    'Authorization': f'Bearer {token}',
                },
            )

        if response.status_code >= 400:
            raise MeliAPIError(f'Mercado Livre API error {response.status_code}: {response.text}')

        return response.json()

    def get_trends(self, site_id: str | None = None) -> list[dict[str, Any]]:
        site = site_id or self.settings.meli_site_id
        response = self._get(f'/trends/{site}', authenticated=True)
        if isinstance(response, list):
            return response
        raise MeliAPIError('Resposta inesperada em /trends.')

    def search_items(
        self,
        query: str,
        site_id: str | None = None,
        offset: int = 0,
        limit: int = DEFAULT_LIMIT,
        extra_params: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        site = site_id or self.settings.meli_site_id
        params = {'q': query, 'offset': offset, 'limit': limit}
        if extra_params:
            params.update(extra_params)

        response = self._get(f'/sites/{site}/search', params=params, authenticated=False)
        if isinstance(response, dict):
            return response
        raise MeliAPIError('Resposta inesperada em /sites/{site}/search.')

    def get_items(self, item_ids: list[str]) -> list[dict[str, Any]]:
        if len(item_ids) > MULTIGET_MAX_ITEMS:
            raise ValueError(f'Máximo de {MULTIGET_MAX_ITEMS} item_ids por multiget.')

        params = {
            'ids': ','.join(item_ids),
            'attributes': (
                'id,title,category_id,domain_id,price,currency_id,available_quantity,'
                'condition,listing_type_id,catalog_listing,permalink,thumbnail,'
                'official_store_id,accepts_mercadopago,buying_mode,status,shipping,'
                'seller_address,attributes,seller_id'
            ),
        }
        response = self._get('/items', params=params, authenticated=False)
        if isinstance(response, list):
            return response
        raise MeliAPIError('Resposta inesperada em /items multiget.')

    def get_category(self, category_id: str) -> dict[str, Any]:
        response = self._get(f'/categories/{category_id}', authenticated=False)
        if isinstance(response, dict):
            return response
        raise MeliAPIError('Resposta inesperada em /categories/{category_id}.')

    def get_category_attributes(self, category_id: str) -> list[dict[str, Any]]:
        response = self._get(f'/categories/{category_id}/attributes', authenticated=False)
        if isinstance(response, list):
            return response
        raise MeliAPIError('Resposta inesperada em /categories/{category_id}/attributes.')
