from __future__ import annotations

from typing import Any

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from app.core.constants import DEFAULT_LIMIT, MULTIGET_MAX_ITEMS
from app.core.exceptions import ConfigurationError, MeliAPIError
from app.core.settings import Settings


class MercadoLivreClient:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._client = httpx.Client(
            base_url=settings.meli_base_url,
            timeout=settings.request_timeout_seconds,
            headers=self._build_headers(),
        )

    def _build_headers(self) -> dict[str, str]:
        headers = {'Accept': 'application/json'}
        if self.settings.meli_access_token:
            headers['Authorization'] = f'Bearer {self.settings.meli_access_token}'
        return headers

    def close(self) -> None:
        self._client.close()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_fixed(1),
        retry=retry_if_exception_type((httpx.HTTPError, MeliAPIError)),
        reraise=True,
    )
    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        response = self._client.get(path, params=params)
        if response.status_code >= 400:
            raise MeliAPIError(f'Mercado Livre API error {response.status_code}: {response.text}')
        return response.json()

    def get_trends(self, site_id: str | None = None) -> list[dict[str, Any]]:
        site = site_id or self.settings.meli_site_id
        if not self.settings.meli_access_token:
            raise ConfigurationError('MELI_ACCESS_TOKEN é necessário para /trends.')
        return self._get(f'/trends/{site}')

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
        return self._get(f'/sites/{site}/search', params=params)

    def get_items(self, item_ids: list[str]) -> list[dict[str, Any]]:
        if len(item_ids) > MULTIGET_MAX_ITEMS:
            raise ValueError(f'Máximo de {MULTIGET_MAX_ITEMS} item_ids por multiget.')
        params = {'ids': ','.join(item_ids), 'attributes': 'id,title,category_id,domain_id,price,currency_id,available_quantity,condition,listing_type_id,catalog_listing,permalink,thumbnail,official_store_id,accepts_mercadopago,buying_mode,status,shipping,seller_address,attributes,seller_id'}
        response = self._get('/items', params=params)
        if isinstance(response, list):
            return response
        raise MeliAPIError('Resposta inesperada em /items multiget.')

    def get_category(self, category_id: str) -> dict[str, Any]:
        return self._get(f'/categories/{category_id}')

    def get_category_attributes(self, category_id: str) -> list[dict[str, Any]]:
        return self._get(f'/categories/{category_id}/attributes')
