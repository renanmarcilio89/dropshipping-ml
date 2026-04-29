from __future__ import annotations

from typing import Any


class OutputPresenter:
    FIELD_LABELS_PT_BR = {
        "count": "quantidade",
        "filters": "filtros",
        "items": "itens",
        "language": "idioma",
        "candidate_id": "candidato_id",
        "candidate_type": "tipo_candidato",
        "term": "termo",
        "normalized_term": "termo_normalizado",
        "predicted_category_id": "categoria_prevista_id",
        "predicted_category_name": "categoria_prevista_nome",
        "category_path_text": "caminho_categoria",
        "category_total_items": "total_itens_categoria",
        "prediction_confidence_score": "pontuacao_confianca_predicao",
        "prediction_confidence_level": "nivel_confianca_predicao",
        "prediction_quality_level": "nivel_qualidade_predicao",
        "prediction_quality_penalty": "penalidade_qualidade_predicao",
        "prediction_quality_reasons": "motivos_qualidade_predicao",
        "term_specificity_level": "nivel_especificidade_termo",
        "listing_allowed": "anuncio_permitido",
        "required_attributes_count": "quantidade_atributos_obrigatorios",
        "important_attributes_count": "quantidade_atributos_importantes",
        "demand_score": "pontuacao_demanda",
        "competition_score": "pontuacao_concorrencia",
        "quality_score": "pontuacao_qualidade",
        "ops_risk_score": "pontuacao_risco_operacional",
        "final_score": "pontuacao_final",
        "score_version": "versao_score",
        "scored_at": "pontuado_em",
        "commercial_score": "pontuacao_comercial",
        "commercial_decision": "decisao_comercial",
        "monetization_fit": "potencial_monetizacao",
        "risk_level": "nivel_risco",
        "recommended_action": "acao_recomendada",
        "reasons": "motivos",
        "missing_data": "dados_faltantes",
        "source": "fonte",
        "analysis_version": "versao_analise",
        "captured_at": "capturado_em",
        "persisted": "persistidos",
        "min_commercial_score": "pontuacao_comercial_minima",
        "min_final_score": "pontuacao_final_minima",
        "confidence_level": "nivel_confianca",
        "max_category_total_items": "maximo_itens_categoria",
        "status": "status",
        "action": "acao",
        "reason_payload": "motivos",
        "candidate": "candidato",
        "created": "criados",
        "updated": "atualizados",
        "skipped": "ignorados",
        "failed": "falhas",
        "errors": "erros",
        "site_id": "site_id",
        "limit": "limite",
        "trend_limit": "limite_tendencias",
        "force": "forcar",
        "sale_price": "preco_venda",
        "supplier_cost": "custo_fornecedor",
        "shipping_cost": "custo_frete",
        "marketplace_fee": "taxa_marketplace",
        "ads_cost": "custo_anuncios",
        "total_cost": "custo_total",
        "estimated_profit": "lucro_estimado",
        "estimated_margin": "margem_estimada",
        "estimated_margin_percent": "margem_estimada_percentual",
        "break_even_price": "preco_break_even",
        "viability_level": "nivel_viabilidade",
        "recommendation": "recomendacao",
        "marketplace_fee_rate": "taxa_marketplace_percentual",
        "ads_cost_rate": "taxa_anuncios_percentual",
        "id": "id",
        "created_at": "criado_em",
        "min_estimated_margin": "margem_estimada_minima",
        "min_estimated_profit": "lucro_estimado_minimo",
        "priority_score": "pontuacao_prioridade",
        "investment_priority": "prioridade_investimento",
        "commercial_recommended_action": "acao_recomendada_comercial",
        "market_reality_recommendation": "recomendacao_realidade_mercado",
        "market_reality_created_at": "realidade_mercado_criada_em",
    }

    VALUE_LABELS_PT_BR = {
        "dropshipping_candidate": "Candidato para dropshipping",
        "affiliate_candidate": "Candidato para afiliados",
        "research_needed": "Precisa de pesquisa",
        "avoid": "Evitar por enquanto",
        "low": "Baixo",
        "medium": "Medio",
        "high": "Alto",
        "none": "Nenhum",
        "unknown": "Desconhecido",
        "open": "Aberto",
        "dismissed": "Descartado",
        "acted": "Acao realizada",
        "product_term": "Termo de produto",
        "pending": "Pendente",
        "qualified": "Qualificado",
        "rejected": "Rejeitado",
        "pending_enrichment": "Pendente de enriquecimento",
        "enriched": "Enriquecido",
        "enrichment_failed": "Falha no enriquecimento",
        "strong": "Forte",
        "viable": "Viavel",
        "thin": "Apertado",
        "weak": "Fraco",
        "unprofitable": "Nao lucrativo",
        "high_priority": "Alta prioridade",
        "controlled_validation": "Validacao controlada",
        "watchlist": "Lista de acompanhamento",
    }

    TEXT_LABELS_PT_BR = {
        "Validate supplier cost, shipping feasibility, marketplace fees, and minimum margin before creating an offer.": "Validar custo do fornecedor, viabilidade de frete, taxas do marketplace e margem minima antes de criar uma oferta.",
        "Validate demand with affiliate links or content before taking supplier, shipping, or inventory exposure.": "Validar demanda com links de afiliado ou conteudo antes de assumir risco com fornecedor, frete ou estoque.",
        "Collect real offer prices, supplier options, fees, shipping constraints, and competitor data before choosing a monetization path.": "Coletar precos reais de ofertas, opcoes de fornecedores, taxas, restricoes de frete e dados de concorrencia antes de escolher uma estrategia de monetizacao.",
        "Do not prioritize this opportunity until the structural risks or prediction quality improve.": "Nao priorizar esta oportunidade ate que os riscos estruturais ou a qualidade da predicao melhorem.",
        "Validate supplier cost, shipping, and margins.": "Validar custo do fornecedor, frete e margens.",
        "Test demand via affiliate links.": "Testar demanda usando links de afiliado.",
        "Collect price, supplier, and competition data.": "Coletar dados de preco, fornecedor e concorrencia.",
        "Ignore for now.": "Ignorar por enquanto.",
        "Strong commercial score based on current structural signals.": "Pontuacao comercial forte com base nos sinais estruturais atuais.",
        "Moderate commercial score that justifies controlled validation.": "Pontuacao comercial moderada, suficiente para uma validacao controlada.",
        "Weak commercial score for immediate monetization.": "Pontuacao comercial fraca para monetizacao imediata.",
        "Prediction quality is reliable enough for commercial investigation.": "A qualidade da predicao e confiavel o suficiente para investigacao comercial.",
        "Prediction quality is not fully classified yet.": "A qualidade da predicao ainda nao esta totalmente classificada.",
        "Prediction quality is weak and reduces confidence.": "A qualidade da predicao e fraca e reduz a confianca.",
        "Operational risk appears low based on available category signals.": "O risco operacional parece baixo com base nos sinais disponiveis da categoria.",
        "Operational risk requires validation before spending money.": "O risco operacional exige validacao antes de investir dinheiro.",
        "Operational risk is high for the current project stage.": "O risco operacional e alto para o estagio atual do projeto.",
        "Affiliate testing can validate demand before supplier or inventory exposure.": "Teste com afiliados pode validar demanda antes de exposicao a fornecedor ou estoque.",
        "Signals are strong enough to investigate supplier-based execution.": "Os sinais sao fortes o suficiente para investigar execucao baseada em fornecedores.",
        "The opportunity needs price, supplier, and fee data before action.": "A oportunidade precisa de dados de preco, fornecedor e taxas antes de qualquer acao.",
        "High commercial score.": "Pontuacao comercial alta.",
        "Moderate commercial score.": "Pontuacao comercial moderada.",
        "Good prediction quality.": "Boa qualidade de predicao.",
        "Low operational risk.": "Baixo risco operacional.",
        "High operational complexity.": "Alta complexidade operacional.",
        "Real offer prices": "Precos reais de ofertas",
        "Estimated marketplace fees": "Taxas estimadas do marketplace",
        "Supplier cost": "Custo do fornecedor",
        "Shipping constraints": "Restricoes de frete",
        "Return and warranty risk": "Risco de devolucao e garantia",
        "Supplier delivery time": "Prazo de entrega do fornecedor",
        "Minimum viable margin": "Margem minima viavel",
        "Competitor offer quality": "Qualidade das ofertas concorrentes",
        "Manual category validation": "Validacao manual da categoria",
        "Marketplace fees": "Taxas do marketplace",
        "Shipping cost": "Custo de frete",
        "Competition pricing": "Preco da concorrencia",
        "Proceed to validate demand, supplier reliability, and fulfillment constraints.": "Prosseguir para validar demanda, confiabilidade do fornecedor e restricoes operacionais.",
        "Proceed with caution and validate acquisition costs before scaling.": "Prosseguir com cautela e validar custos de aquisicao antes de escalar.",
        "Only proceed if demand is strong or if costs can be reduced.": "Prosseguir apenas se a demanda for forte ou se os custos puderem ser reduzidos.",
        "Do not prioritize unless supplier cost, fees, or shipping can improve.": "Nao priorizar a menos que custo de fornecedor, taxas ou frete possam melhorar.",
        "Avoid this scenario because estimated profit is negative or zero.": "Evitar este cenario porque o lucro estimado e negativo ou zero.",
        "Prioritize validation with supplier, pricing, demand test, and operating constraints.": "Priorizar validacao com fornecedor, precificacao, teste de demanda e restricoes operacionais.",
        "Run a controlled validation before committing capital or operational exposure.": "Executar validacao controlada antes de comprometer capital ou exposicao operacional.",
        "Keep monitoring and improve margin, demand evidence, or operational conditions before acting.": "Continuar monitorando e melhorar margem, evidencia de demanda ou condicoes operacionais antes de agir.",
        "Do not prioritize this opportunity under the current market reality scenario.": "Nao priorizar esta oportunidade no cenario atual de realidade de mercado.",
        "Validate supplier cost, shipping, marketplace fees, delivery time, and minimum viable margin before creating an offer.": "Validar custo do fornecedor, frete, taxas do marketplace, prazo de entrega e margem minima viavel antes de criar uma oferta.",
        "Validate supplier cost, shipping feasibility, marketplace fees, and minimum margin before creating an offer.": "Validar custo do fornecedor, viabilidade de frete, taxas do marketplace e margem minima antes de criar uma oferta.",
        "Research affiliate programs, content angles, and offer availability before taking inventory exposure.": "Pesquisar programas de afiliados, angulos de conteudo e disponibilidade de ofertas antes de assumir exposicao com estoque.",
        "Collect real offer prices, supplier options, fees, shipping constraints, and demand evidence before choosing a monetization path.": "Coletar precos reais de ofertas, opcoes de fornecedores, taxas, restricoes de frete e evidencias de demanda antes de escolher uma estrategia de monetizacao.",
        "Do not prioritize this opportunity until the structural risks or prediction quality improve.": "Nao priorizar esta oportunidade ate que os riscos estruturais ou a qualidade da predicao melhorem.",
    }

    @classmethod
    def present(cls, payload: Any, *, language: str) -> Any:
        normalized_language = cls.normalize_language(language)

        if normalized_language == "en":
            return payload

        return cls._present_pt_br(payload)

    @staticmethod
    def normalize_language(language: str) -> str:
        normalized = language.strip()

        if normalized in {"en", "pt-BR"}:
            return normalized

        raise ValueError("language invalido. Use: en ou pt-BR.")

    @classmethod
    def _present_pt_br(cls, payload: Any) -> Any:
        if isinstance(payload, list):
            return [cls._present_pt_br(item) for item in payload]

        if isinstance(payload, dict):
            return {
                cls.FIELD_LABELS_PT_BR.get(key, key): cls._present_pt_br(value)
                for key, value in payload.items()
            }

        if isinstance(payload, str):
            return cls.TEXT_LABELS_PT_BR.get(
                payload,
                cls.VALUE_LABELS_PT_BR.get(payload, payload),
            )

        return payload
