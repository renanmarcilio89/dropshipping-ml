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

    ACTIONS_PT_BR = {
        "Validate supplier cost, shipping feasibility, marketplace fees, and minimum margin before creating an offer.": "Validar custo do fornecedor, viabilidade de frete, taxas do marketplace e margem mínima antes de criar uma oferta.",
        "Validate demand with affiliate links or content before taking supplier, shipping, or inventory exposure.": "Validar demanda com links de afiliado ou conteúdo antes de assumir risco com fornecedor, frete ou estoque.",
        "Collect real offer prices, supplier options, fees, shipping constraints, and competitor data before choosing a monetization path.": "Coletar preços reais de ofertas, opções de fornecedores, taxas, restrições de frete e dados de concorrência antes de escolher uma estratégia de monetização.",
        "Do not prioritize this opportunity until the structural risks or prediction quality improve.": "Não priorizar esta oportunidade até que os riscos estruturais ou a qualidade da predição melhorem.",
        "Validate supplier cost, shipping, and margins.": "Validar custo do fornecedor, frete e margens.",
        "Test demand via affiliate links.": "Testar demanda usando links de afiliado.",
        "Collect price, supplier, and competition data.": "Coletar dados de preço, fornecedor e concorrência.",
        "Ignore for now.": "Ignorar por enquanto.",
    }

    REASONS_PT_BR = {
        "Strong commercial score based on current structural signals.": "Pontuação comercial forte com base nos sinais estruturais atuais.",
        "Moderate commercial score that justifies controlled validation.": "Pontuação comercial moderada, suficiente para uma validação controlada.",
        "Weak commercial score for immediate monetization.": "Pontuação comercial fraca para monetização imediata.",
        "Prediction quality is reliable enough for commercial investigation.": "A qualidade da predição é confiável o suficiente para investigação comercial.",
        "Prediction quality is not fully classified yet.": "A qualidade da predição ainda não está totalmente classificada.",
        "Prediction quality is weak and reduces confidence.": "A qualidade da predição é fraca e reduz a confiança.",
        "Operational risk appears low based on available category signals.": "O risco operacional parece baixo com base nos sinais disponíveis da categoria.",
        "Operational risk requires validation before spending money.": "O risco operacional exige validação antes de investir dinheiro.",
        "Operational risk is high for the current project stage.": "O risco operacional é alto para o estágio atual do projeto.",
        "Affiliate testing can validate demand before supplier or inventory exposure.": "Teste com afiliados pode validar demanda antes de exposição a fornecedor ou estoque.",
        "Signals are strong enough to investigate supplier-based execution.": "Os sinais são fortes o suficiente para investigar execução baseada em fornecedores.",
        "The opportunity needs price, supplier, and fee data before action.": "A oportunidade precisa de dados de preço, fornecedor e taxas antes de qualquer ação.",
        "High commercial score.": "Pontuação comercial alta.",
        "Moderate commercial score.": "Pontuação comercial moderada.",
        "Good prediction quality.": "Boa qualidade de predição.",
        "Low operational risk.": "Baixo risco operacional.",
        "High operational complexity.": "Alta complexidade operacional.",
    }

    MISSING_DATA_PT_BR = {
        "Real offer prices": "Preços reais de ofertas",
        "Estimated marketplace fees": "Taxas estimadas do marketplace",
        "Supplier cost": "Custo do fornecedor",
        "Shipping constraints": "Restrições de frete",
        "Return and warranty risk": "Risco de devolução e garantia",
        "Supplier delivery time": "Prazo de entrega do fornecedor",
        "Minimum viable margin": "Margem mínima viável",
        "Competitor offer quality": "Qualidade das ofertas concorrentes",
        "Manual category validation": "Validação manual da categoria",
        "Marketplace fees": "Taxas do marketplace",
        "Shipping cost": "Custo de frete",
        "Competition pricing": "Preço da concorrência",
    }

    @classmethod
    def present_many(
        cls,
        items: list[dict[str, Any]],
        *,
        language: str,
    ) -> list[dict[str, Any]]:
        normalized_language = cls.normalize_language(language)

        if normalized_language == "en":
            return items

        return [cls.present_pt_br(item) for item in items]

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
            "potencial_de_monetizacao": cls.MONETIZATION_LABELS_PT_BR.get(
                item["monetization_fit"],
                item["monetization_fit"],
            ),
            "nivel_de_risco": cls.RISK_LABELS_PT_BR.get(
                item["risk_level"],
                item["risk_level"],
            ),
            "acao_recomendada": cls.translate_action(item["recommended_action"]),
            "motivos": cls.translate_list(item["reasons"], cls.REASONS_PT_BR),
            "dados_faltantes": cls.translate_list(
                item["missing_data"],
                cls.MISSING_DATA_PT_BR,
            ),
            "fonte": item["source"],
            "versao_analise": item["analysis_version"],
            "capturado_em": item["captured_at"],
        }

    @classmethod
    def translate_action(cls, value: str) -> str:
        return cls.ACTIONS_PT_BR.get(value, value)

    @classmethod
    def translate_list(cls, values: list[str], mapping: dict[str, str]) -> list[str]:
        return [mapping.get(value, value) for value in values]

    @staticmethod
    def normalize_language(language: str) -> str:
        normalized = language.strip()

        if normalized in {"en", "pt-BR"}:
            return normalized

        raise ValueError("language inválido. Use: en ou pt-BR.")
