# dropshipping-ml

Pipeline modular em Python para construção de um agente de inteligência de mercado no Mercado Livre.

O objetivo deste projeto é identificar oportunidades de venda (dropshipping e afiliados) com base em sinais reais de demanda, concorrência e qualidade de mercado — **sem atuar como seller nesta fase inicial**.

---

## 🎯 Objetivo do sistema

Construir um pipeline que:

1. Descobre demanda (trends)
2. Gera candidatos de produto/nicho
3. Qualifica candidatos (filtrando itens inviáveis)
4. Enriquece candidatos com dados de mercado
5. Calcula score de oportunidade
6. Gera alertas acionáveis

---

## 🚨 Escopo atual (muito importante)

Este projeto **não é**, neste momento:

* um integrador de seller
* um sincronizador de catálogo próprio
* um gerenciador de anúncios
* um sistema baseado em `/users/{user_id}/items/search`

O foco atual é **exclusivamente inteligência de mercado**.

---

## 🧠 Filosofia do projeto

* API-first (uso da API oficial do Mercado Livre)
* Persistência de payload bruto para auditoria
* Pipeline incremental e reprocessável
* Separação clara entre:

  * jobs (orquestração)
  * services (regra de negócio)
  * repositories (acesso a dados)

---

## 🧱 Arquitetura

O projeto segue uma arquitetura modular baseada em:

```text
CLI (Typer)
  ↓
Jobs (orquestração do pipeline)
  ↓
Services (lógica de negócio)
  ↓
Repositories (persistência)
  ↓
Banco de dados (PostgreSQL)
```

### Componentes principais

* **Jobs** → executam etapas do pipeline
* **Services** → contêm regras e transformações
* **Repositories** → abstraem acesso ao banco
* **Models** → definem estrutura de dados
* **Clients** → integração com API do Mercado Livre

---

## 🔄 Pipeline atual

```text
sync-trends → build-candidates → qualify-candidates
```

### ✔ Etapas implementadas

#### 1. Trends ingestion (`sync-trends`)

* Coleta termos de trends da API
* Salva payload bruto (`api_payload`)
* Cria snapshots (`trend_snapshot`)

#### 2. Candidate generation (`build-candidates`)

* Normalização de termos
* Deduplicação
* Criação de candidatos (`candidate`)

#### 3. Candidate qualification (`qualify-candidates`)

Classificação baseada em heurísticas:

* `approved` → elegível para enriquecimento
* `rejected` → descartado
* `needs_review` → análise manual futura

---

## 🔜 Próximas etapas

```text
sync-trends
  → build-candidates
  → qualify-candidates
  → enrich-candidates
  → score-candidates
  → generate-alerts
```

### Próximo passo imediato

👉 `enrich-candidates`

Responsável por:

* coletar sinais de mercado reais
* analisar concorrência
* identificar padrões de preço e oferta
* preparar base para scoring

---

## 🗃️ Modelo de dados (resumo)

### candidate

Representa um possível produto ou nicho.

Campos principais:

* `source_term`
* `normalized_term`
* `status`
* `qualification_status`
* `qualification_reason`
* `first_seen_at`
* `last_seen_at`

---

### trend_snapshot

* termos coletados de trends
* posição no ranking
* timestamp de captura

---

### api_payload

* payload bruto da API
* usado para:

  * auditoria
  * reprocessamento
  * debugging

---

### opportunity_score (futuro)

* demand_score
* competition_score
* quality_score
* ops_risk_score
* final_score

---

## ⚙️ Stack

* Python 3.12
* SQLAlchemy 2.x
* Alembic
* PostgreSQL
* httpx
* Pydantic v2
* Typer
* structlog
* pytest

---

## 🧪 Execução via CLI

```bash
python -m app.main health

python -m app.main sync-trends

python -m app.main build-candidates

python -m app.main qualify-candidates
```

---

## 🔐 Autenticação Mercado Livre

Fluxo baseado em OAuth:

1. Obter authorization code
2. Trocar por access_token
3. Persistir no banco
4. Refresh automático quando necessário

Comando disponível:

```bash
python -m app.main auth-bootstrap "<authorization_code>"
```

---

## 💾 Banco de dados

* PostgreSQL
* Controle de schema via Alembic
* Armazenamento de:

  * candidatos
  * trends
  * payloads brutos
  * (futuro) snapshots de mercado e scoring

---

## 🧩 Princípios importantes

* **Jobs controlam transação (commit/rollback)**
* **Repositories não fazem commit**
* **Normalização centralizada**
* **Estados explícitos (sem strings mágicas espalhadas)**
* **Pipeline sempre reprocessável**

---

## 📌 Roadmap técnico

* [x] Trends ingestion
* [x] Candidate generation
* [x] Candidate qualification
* [ ] Candidate enrichment
* [ ] Opportunity scoring
* [ ] Alert engine

---

## 📎 Observação final

Este projeto foi desenhado para evoluir de forma incremental.

A prioridade não é operar como seller imediatamente, mas sim construir uma **camada sólida de inteligência de mercado**, capaz de identificar oportunidades reais antes de qualquer execução operacional.

---
