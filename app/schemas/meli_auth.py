from datetime import datetime

from pydantic import BaseModel


class OAuthTokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    scope: str | None = None
    user_id: int | None = None
    refresh_token: str


class CurrentUserResponse(BaseModel):
    id: int
    nickname: str | None = None


class StoredCredential(BaseModel):
    user_id: int | None = None
    nickname: str | None = None
    access_token: str
    refresh_token: str
    token_type: str | None = None
    scope: str | None = None
    expires_at: datetime
