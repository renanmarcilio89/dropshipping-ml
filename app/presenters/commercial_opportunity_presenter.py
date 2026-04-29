from typing import Any


class CommercialOpportunityPresenter:
    DECISION_LABELS_PT_BR = {
        "dropshipping_candidate": "Candidato para dropshipping",
        "affiliate_candidate": "Candidato para afiliados",
        "research_needed": "Precisa de pesquisa",
        "avoid": "Evitar por enquanto",
    }

    RISK_LABELS_PT_BR = {
        "low": "Baixo",
        "medium": "Médio",
        "high": "Alto",
    }

    MONETIZATION_LABELS_PT_BR = {
        "low": "Baixo",
        "medium": "Médio",
        "high": "Alto",
    }

    @classmethod
    def present_many(
        cls,
        items: list[dict[str, Any]],
        *,
        language: str,
    ) -> list[dict[str, Any]]:
        if language == "en":
            return items

        if language == "pt-BR":
            return [cls.present_pt_br(item) for item in items]

        raise ValueError("language inválido. Use: en ou pt-BR.")

    @classmethod
    def present_pt_br(cls, item: dict[str, Any]) -> dict[str, Any]:
        return {
            "id": item["id"],
            "candidato_id": item["candidate_id"],
            "pontuacao_comercial": item["commercial_score"],
            "decisao_comercial": cls.DECISION_LABELS_PT_BR.get(
                item["commercial_decision"],
                item["commercial_decision"],
            ),
            "decisao_comercial_codigo": item["commercial_decision"],
            "potencial_de_monetizacao": cls.MONETIZATION_LABELS_PT_BR.get(
                item["monetization_fit"],
                item["monetization_fit"],
            ),
            "potencial_de_monetizacao_codigo": item["monetization_fit"],
            "nivel_de_risco": cls.RISK_LABELS_PT_BR.get(
                item["risk_level"],
                item["risk_level"],
            ),
            "nivel_de_risco_codigo": item["risk_level"],
            "acao_recomendada": item["recommended_action"],
            "motivos": item["reasons"],
            "dados_faltantes": item["missing_data"],
            "fonte": item["source"],
            "versao_analise": item["analysis_version"],
            "capturado_em": item["captured_at"],
        }
