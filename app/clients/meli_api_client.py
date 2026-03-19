from datetime import UTC, datetime

import httpx
from sqlalchemy.orm import Session

from app.core.settings import settings
from app.repositories.meli_credentials import MeliCredentialRepository
from app.services.meli_auth_service import MeliAuthService


class MeliApiClient:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.repo = MeliCredentialRepository(session)
        self.auth_service = MeliAuthService()
        self.base_url = settings.meli_base_url.rstrip("/")
        self.timeout = settings.request_timeout_seconds

    def get(self, path: str, params: dict | None = None) -> dict:
        access_token = self._get_valid_access_token()

        with httpx.Client(timeout=self.timeout) as client:
            response = client.get(
                f"{self.base_url}{path}",
                params=params,
                headers={"Authorization": f"Bearer {access_token}"},
            )

            if response.status_code == 401:
                access_token = self._refresh_and_get_access_token()
                response = client.get(
                    f"{self.base_url}{path}",
                    params=params,
                    headers={"Authorization": f"Bearer {access_token}"},
                )

            response.raise_for_status()
            return response.json()

    def _get_valid_access_token(self) -> str:
        credential = self.repo.get_active()

        if credential is None:
            if settings.meli_access_token and settings.meli_refresh_token:
                token_data = self.auth_service.refresh_access_token(settings.meli_refresh_token)
                user = self.auth_service.get_current_user(token_data.access_token)
                stored = self.repo.upsert_tokens(
                    token_data=token_data,
                    expires_at=self.auth_service.calculate_expires_at(token_data.expires_in),
                    nickname=user.nickname,
                )
                return stored.access_token
            raise RuntimeError("No stored Mercado Livre credentials found.")

        now = datetime.now(UTC).replace(tzinfo=None)
        expires_at = credential.expires_at.replace(tzinfo=None)

        if expires_at <= now:
            return self._refresh_and_get_access_token()

        return credential.access_token

    def _refresh_and_get_access_token(self) -> str:
        credential = self.repo.get_active()
        if credential is None:
            raise RuntimeError("No stored Mercado Livre credentials available for refresh.")

        token_data = self.auth_service.refresh_access_token(credential.refresh_token)
        user = self.auth_service.get_current_user(token_data.access_token)

        stored = self.repo.upsert_tokens(
            token_data=token_data,
            expires_at=self.auth_service.calculate_expires_at(token_data.expires_in),
            nickname=user.nickname,
        )
        return stored.access_token
