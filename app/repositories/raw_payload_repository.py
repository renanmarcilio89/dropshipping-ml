from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.raw import ApiPayload


class RawPayloadRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def save(
        self,
        *,
        source_name: str,
        endpoint: str,
        payload: dict | list,
        payload_hash: str,
        captured_at: datetime,
        request_params: dict | None = None,
        site_id: str | None = None,
    ) -> ApiPayload:
        stmt = select(ApiPayload).where(ApiPayload.payload_hash == payload_hash)
        existing = self.session.execute(stmt).scalars().first()
        if existing is not None:
            return existing

        row = ApiPayload(
            source_name=source_name,
            site_id=site_id,
            endpoint=endpoint,
            request_params=request_params,
            payload=payload,
            payload_hash=payload_hash,
            captured_at=captured_at,
        )
        self.session.add(row)
        self.session.flush()
        self.session.refresh(row)
        return row
