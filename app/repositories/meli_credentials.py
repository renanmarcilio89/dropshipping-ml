from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.auth import MeliCredential
from app.schemas.meli_auth import OAuthTokenResponse


class MeliCredentialRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_active(self) -> MeliCredential | None:
        stmt = select(MeliCredential).order_by(MeliCredential.updated_at.desc(), MeliCredential.id.desc())
        return self.session.execute(stmt).scalars().first()

    def upsert_tokens(
        self,
        token_data: OAuthTokenResponse,
        expires_at,
        nickname: str | None = None,
    ) -> MeliCredential:
        credential = None

        if token_data.user_id is not None:
            stmt = select(MeliCredential).where(MeliCredential.user_id == token_data.user_id)
            credential = self.session.execute(stmt).scalars().first()

        if credential is None:
            credential = self.get_active()

        if credential is None:
            credential = MeliCredential(
                user_id=token_data.user_id,
                nickname=nickname,
                access_token=token_data.access_token,
                refresh_token=token_data.refresh_token,
                token_type=token_data.token_type,
                scope=token_data.scope,
                expires_at=expires_at,
            )
            self.session.add(credential)
        else:
            credential.user_id = token_data.user_id
            credential.nickname = nickname
            credential.access_token = token_data.access_token
            credential.refresh_token = token_data.refresh_token
            credential.token_type = token_data.token_type
            credential.scope = token_data.scope
            credential.expires_at = expires_at

        self.session.commit()
        self.session.refresh(credential)
        return credential
