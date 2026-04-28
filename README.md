# dropshipping-ml

Pipeline modular em Python para construção de um agente de inteligência de mercado no Mercado Livre.

O objetivo do projeto é identificar oportunidades de venda, dropshipping e afiliados com base em sinais de demanda, estrutura de categoria, qualidade da predição, concorrência estrutural e risco operacional — **sem atuar como seller nesta fase inicial**.

---

## Objetivo do sistema

Construir um pipeline que:

1. Descobre demanda a partir de trends
2. Gera candidatos de produto ou nicho
3. Qualifica candidatos com heurísticas iniciais
4. Enriquece candidatos com dados estruturais da API do Mercado Livre
5. Avalia a qualidade semântica da predição de categoria/domínio
6. Calcula score de oportunidade
7. Ranqueia oportunidades
8. Gera alertas acionáveis com explicabilidade

---

## Escopo atual

Este projeto **não é**, neste momento:

* um integrador de seller
* um sincronizador de catálogo próprio
* um gerenciador de anúncios
* um sistema operacional de publicação de anúncios
* um pipeline baseado em `/users/{user_id}/items/search`

O foco atual é **inteligência de mercado e priorização de oportunidades**.

Importante: o endpoint público `/sites/{site_id}/search` retornou `403 Forbidden` nos testes atuais, mesmo com Bearer Token. Por isso, a etapa de análise de anúncios reais ainda não faz parte do pipeline principal. A inteligência atual usa endpoints que estão funcionando no ambiente atual:

* `/trends/{site_id}`
* `/sites/{site_id}/domain_discovery/search`
* `/categories/{category_id}`
* `/categories/{category_id}/attributes`

---

## Filosofia do projeto

* API-first, usando API oficial do Mercado Livre sempre que disponível
* Persistência de payload bruto para auditoria, debugging e reprocessamento
* Pipeline incremental e reprocessável
* Separação clara entre:
  * jobs: orquestração do pipeline
  * services: regras de negócio
  * repositories: acesso ao banco
  * models: estrutura persistida
  * clients: integração com APIs externas
* Jobs controlam transação
* Repositories não fazem commit
* Estados explícitos para candidatos
* Normalização centralizada de termos

---

## Commercial Intelligence Layer

A camada de inteligência comercial transforma oportunidades técnicas em decisões mais próximas de ação comercial.

Ela reaproveita o ranking estrutural gerado pelo pipeline e classifica cada oportunidade em uma das seguintes decisões:

- `dropshipping_candidate`: oportunidade com sinais suficientes para validar fornecedor, frete, taxas e margem.
- `affiliate_candidate`: oportunidade indicada para validação com afiliados ou conteúdo antes de exposição operacional.
- `research_needed`: oportunidade promissora, mas ainda dependente de dados adicionais.
- `avoid`: oportunidade que não deve ser priorizada no momento.

A análise comercial considera:

- score estrutural da oportunidade;
- qualidade da predição;
- risco operacional;
- complexidade da categoria;
- quantidade de atributos obrigatórios;
- sinais heurísticos de preço;
- dados ausentes necessários para validação comercial.

As análises comerciais são persistidas em `commercial_opportunity_analysis`, permitindo histórico e comparação futura.

### Comandos

```bash
uv run python -m app.main commercial-opportunities
```

---

## Pipeline atual

```text
sync-trends
  ↓
build-candidates
  ↓
qualify-candidates
  ↓
enrich-candidates
  ↓
score-candidates
  ↓
rank-opportunities
  ↓
alert-opportunities
  ↓
commercial-opportunities
  ↓
list-commercial-analyses
```

---

## Arquitetura

```text
CLI (Typer)
  ↓
Jobs (orquestração)
  ↓
Services (regras de negócio)
  ↓
Repositories (persistência)
  ↓
Models / PostgreSQL
  ↓
Mercado Livre API