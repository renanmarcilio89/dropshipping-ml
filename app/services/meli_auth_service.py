from datetime import UTC, datetime, timedelta

import httpx

from app.core.settings import settings
from app.schemas.meli_auth import CurrentUserResponse, OAuthTokenResponse


class MeliAuthService:
    def __init__(self) -> None:
        self.base_url = settings.meli_base_url.rstrip("/")
        self.timeout = settings.request_timeout_seconds

    def exchange_code_for_token(self, code: str) -> OAuthTokenResponse:
        self._validate_static_credentials()

        payload = {
            "grant_type": "authorization_code",
            "client_id": settings.meli_app_id,
            "client_secret": settings.meli_client_secret,
            "code": code,
            "redirect_uri": settings.meli_redirect_uri,
        }

        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/oauth/token",
                data=payload,
                headers={
                    "accept": "application/json",
                    "content-type": "application/x-www-form-urlencoded",
                },
            )

            if response.is_error:
                raise RuntimeError(
                    f"Token exchange failed: status={response.status_code} body={response.text}"
                )

            return OAuthTokenResponse.model_validate(response.json())

    def refresh_access_token(self, refresh_token: str) -> OAuthTokenResponse:
        self._validate_static_credentials()

        payload = {
            "grant_type": "refresh_token",
            "client_id": settings.meli_app_id,
            "client_secret": settings.meli_client_secret,
            "refresh_token": refresh_token,
        }

        with httpx.Client(timeout=self.timeout) as client:
            response = client.post(
                f"{self.base_url}/oauth/token",
                data=payload,
                headers={
                    "accept": "application/json",
                    "content-type": "application/x-www-form-urlencoded",
                },
            )

            if response.is_error:
                raise RuntimeError(
                    f"Token refresh failed: status={response.status_code} body={response.text}"
                )

            return OAuthTokenResponse.model_validate(response.json())

    def get_current_user(self, access_token: str) -> CurrentUserResponse:
        with httpx.Client(timeout=self.timeout) as client:
            response = client.get(
                f"{self.base_url}/users/me",
                headers={"Authorization": f"Bearer {access_token}"},
            )
            response.raise_for_status()
            return CurrentUserResponse.model_validate(response.json())

    @staticmethod
    def calculate_expires_at(expires_in: int) -> datetime:
        return datetime.now(UTC) + timedelta(seconds=max(expires_in - 60, 0))

    @staticmethod
    def _validate_static_credentials() -> None:
        missing = []
        if not settings.meli_app_id:
            missing.append("MELI_APP_ID")
        if not settings.meli_client_secret:
            missing.append("MELI_CLIENT_SECRET")
        if not settings.meli_redirect_uri:
            missing.append("MELI_REDIRECT_URI")

        if missing:
            raise RuntimeError(f"Missing required settings: {', '.join(missing)}")
