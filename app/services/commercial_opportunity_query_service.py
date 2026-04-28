from app.models.market import CommercialOpportunityAnalysis


class CommercialOpportunityQueryService:
    @staticmethod
    def build_output(
        analyses: list[CommercialOpportunityAnalysis],
    ) -> list[dict]:
        return [
            {
                "id": analysis.id,
                "candidate_id": analysis.candidate_id,
                "commercial_score": float(analysis.commercial_score),
                "commercial_decision": analysis.commercial_decision,
                "monetization_fit": analysis.monetization_fit,
                "risk_level": analysis.risk_level,
                "recommended_action": analysis.recommended_action,
                "reasons": analysis.reason_payload,
                "missing_data": analysis.missing_data_payload,
                "source": analysis.source_payload,
                "analysis_version": analysis.analysis_version,
                "captured_at": analysis.captured_at.isoformat()
                if analysis.captured_at
                else None,
            }
            for analysis in analyses
        ]

    @staticmethod
    def normalize_commercial_decision(value: str | None) -> str | None:
        if value is None:
            return None

        normalized = value.strip().lower()
        allowed = {
            "dropshipping_candidate",
            "affiliate_candidate",
            "research_needed",
            "avoid",
        }

        if normalized in allowed:
            return normalized

        raise ValueError(
            "commercial_decision inválido. Use: dropshipping_candidate, affiliate_candidate, research_needed ou avoid."
        )

    @staticmethod
    def normalize_risk_level(value: str | None) -> str | None:
        if value is None:
            return None

        normalized = value.strip().lower()
        allowed = {"low", "medium", "high"}

        if normalized in allowed:
            return normalized

        raise ValueError("risk_level inválido. Use: low, medium ou high.")
