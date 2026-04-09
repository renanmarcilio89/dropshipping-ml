from __future__ import annotations

from typing import Any


class OpportunityAlertQueryService:
    VALID_STATUSES = {"open", "dismissed", "acted"}
    VALID_CONFIDENCE_LEVELS = {"high", "medium", "low", "none"}

    def normalize_status(self, value: str | None) -> str | None:
        if value is None:
            return None

        normalized = value.strip().lower()
        if normalized not in self.VALID_STATUSES:
            raise ValueError("status inválido. Use: open, dismissed ou acted.")

        return normalized

    def normalize_confidence_level(self, value: str | None) -> str | None:
        if value is None:
            return None

        normalized = value.strip().lower()
        if normalized not in self.VALID_CONFIDENCE_LEVELS:
            raise ValueError(
                "confidence_level inválido. Use: high, medium, low ou none."
            )

        return normalized

    def build_output(self, rows: list[Any]) -> list[dict]:
        output: list[dict] = []

        for row in rows:
            output.append(
                {
                    "alert_id": row.id,
                    "candidate_id": row.candidate_id,
                    "alert_version": row.alert_version,
                    "score_version": row.score_version,
                    "final_score": self._to_float(row.final_score),
                    "confidence_level": row.confidence_level,
                    "category_id": row.category_id,
                    "category_name": row.category_name,
                    "action": row.action,
                    "reasons": row.reason_payload,
                    "status": row.status,
                    "created_at": row.created_at.isoformat() if row.created_at else None,
                }
            )

        return output

    @staticmethod
    def _to_float(value: Any) -> float | None:
        if value is None:
            return None
        return float(value)
