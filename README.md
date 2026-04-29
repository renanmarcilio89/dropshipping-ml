# dropshipping-ml

Pipeline modular em Python para construcao de um agente de inteligencia de mercado no Mercado Livre.

O objetivo do projeto e identificar oportunidades de venda, dropshipping e afiliados com base em sinais de demanda, estrutura de categoria, qualidade da predicao, concorrencia estrutural e risco operacional.

Nesta fase, o projeto ainda nao atua como seller, nao publica anuncios e nao gerencia catalogo proprio. O foco atual e inteligencia de mercado, priorizacao de oportunidades, suporte a decisao comercial e construcao de historico analitico.

---

## Objetivo do sistema

Construir um pipeline que:

1. Descobre demanda a partir de trends.
2. Gera candidatos de produto ou nicho.
3. Qualifica candidatos com heuristicas iniciais.
4. Enriquece candidatos com dados estruturais da API do Mercado Livre.
5. Avalia a qualidade semantica da predicao de categoria e dominio.
6. Calcula score de oportunidade.
7. Ranqueia oportunidades.
8. Gera alertas acionaveis com explicabilidade.
9. Transforma oportunidades tecnicas em analises comerciais.
10. Persiste historico de decisoes comerciais para comparacao futura.
11. Permite output localizado em ingles ou portugues sem acentos.

---

## Escopo atual

Este projeto nao e, neste momento:

- um integrador de seller;
- um sincronizador de catalogo proprio;
- um gerenciador de anuncios;
- um sistema operacional de publicacao de anuncios;
- um pipeline baseado em `/users/{user_id}/items/search`.

O foco atual e inteligencia de mercado e priorizacao de oportunidades.

Importante: o endpoint publico `/sites/{site_id}/search` retornou `403 Forbidden` nos testes atuais, mesmo com Bearer Token. Por isso, a etapa de analise de anuncios reais ainda nao faz parte do pipeline principal.

A inteligencia atual usa endpoints que estao funcionando no ambiente atual:

- `/trends/{site_id}`
- `/sites/{site_id}/domain_discovery/search`
- `/categories/{category_id}`
- `/categories/{category_id}/attributes`

---

## Filosofia do projeto

- API-first, usando API oficial do Mercado Livre sempre que disponivel.
- Persistencia de payload bruto para auditoria, debugging e reprocessamento.
- Pipeline incremental e reprocessavel.
- Separacao clara entre jobs, services, repositories, models, clients e presenters.
- Jobs controlam transacao.
- Repositories nao fazem commit.
- Estados explicitos para candidatos.
- Normalizacao centralizada de termos.
- Codigo, entidades internas e valores persistidos em ingles.
- Output localizado apenas na camada de apresentacao.
- Saidas em portugues evitam acentos para reduzir problemas em reports, CSVs e integracoes externas.

---

## Arquitetura

    CLI (Typer)
      ↓
    Jobs (orquestracao)
      ↓
    Services (regras de negocio)
      ↓
    Repositories (persistencia)
      ↓
    Models / PostgreSQL
      ↓
    Mercado Livre API

A camada de apresentacao fica separada:

    Jobs / Services
      ↓
    Payload interno em ingles
      ↓
    OutputPresenter
      ↓
    JSON em ingles ou pt-BR sem acentos

---

## Pipeline atual

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

---

## Stack

- Python
- Typer
- SQLAlchemy
- Alembic
- PostgreSQL
- Pydantic
- httpx
- Mercado Livre API
- uv

---

## Estrutura principal

    app/
      clients/
      core/
      db/
      jobs/
      models/
      presenters/
      repositories/
      schemas/
      scoring/
      services/
    alembic/
      versions/
    tests/
    README.md
    pyproject.toml

---

## Setup local

### 1. Entrar no diretorio do projeto

    cd C:\Users\Renan\workspace\mercadolivre_ml_pipeline

### 2. Ativar ambiente virtual no PowerShell

    .venv\Scripts\Activate.ps1

### 3. Instalar dependencias

    uv sync

### 4. Verificar saude da aplicacao

    uv run python -m app.main health

Saida esperada:

    ok

---

## Variaveis de ambiente

O projeto utiliza `.env` para configuracoes locais.

Exemplo de variavel de banco:

    DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/mercadolivre_ml

Para uso direto com `psql`, a URL deve ficar sem `+psycopg`:

    postgresql://postgres:postgres@localhost:5432/mercadolivre_ml

---

## Banco de dados

### Abrir banco com psql usando URL direta

    psql "postgresql://postgres:postgres@localhost:5432/mercadolivre_ml"

### Rodar query direta no PowerShell

    psql "postgresql://postgres:postgres@localhost:5432/mercadolivre_ml" -c "select * from alembic_version;"

### Ver tabelas

Dentro do `psql`:

    \dt

### Sair do psql

    \q

### Ver revision atual do Alembic direto no banco

    psql "postgresql://postgres:postgres@localhost:5432/mercadolivre_ml" -c "select * from alembic_version;"

### Ver ultimas analises comerciais persistidas

    psql "postgresql://postgres:postgres@localhost:5432/mercadolivre_ml" -c "select candidate_id, commercial_score, commercial_decision, risk_level, analysis_version, captured_at from commercial_opportunity_analysis order by captured_at desc limit 20;"

### Verificar se uma tabela existe

    psql "postgresql://postgres:postgres@localhost:5432/mercadolivre_ml" -c "select to_regclass('public.commercial_opportunity_analysis');"

---

## Alembic

O projeto usa Alembic para versionamento do banco.

### Aplicar migrations

    uv run alembic upgrade head

### Ver revision atual

    uv run alembic current

### Ver head atual

    uv run alembic heads

### Ver historico de migrations

    uv run alembic history

### Criar nova migration vazia

    uv run alembic revision -m "add some feature"

### Criar migration por autogenerate

    uv run alembic revision --autogenerate -m "add some feature"

### Corrigir revision registrada no banco quando necessario

Use apenas quando a tabela `alembic_version` estiver apontando para uma revision que nao existe mais nos arquivos locais.

Exemplo usado durante o desenvolvimento:

    psql "postgresql://postgres:postgres@localhost:5432/mercadolivre_ml" -c "update alembic_version set version_num = 'ef5796c86bb5';"

Depois aplicar migrations normalmente:

    uv run alembic upgrade head

---

## Fluxo de execucao do motor

### 1. Sincronizar trends

    uv run python -m app.main sync-trends

Com output em portugues sem acentos:

    uv run python -m app.main sync-trends --language pt-BR

### 2. Construir candidatos

    uv run python -m app.main build-candidates

Com limite de trends:

    uv run python -m app.main build-candidates --trend-limit 100

Com output em portugues sem acentos:

    uv run python -m app.main build-candidates --language pt-BR

### 3. Qualificar candidatos

    uv run python -m app.main qualify-candidates

Com limite:

    uv run python -m app.main qualify-candidates --limit 100

Com output em portugues sem acentos:

    uv run python -m app.main qualify-candidates --language pt-BR

### 4. Enriquecer candidatos

    uv run python -m app.main enrich-candidates

Com limite:

    uv run python -m app.main enrich-candidates --limit 20

Forcando reprocessamento:

    uv run python -m app.main enrich-candidates --limit 20 --force

Com output em portugues sem acentos:

    uv run python -m app.main enrich-candidates --limit 20 --language pt-BR

### 5. Calcular scores

    uv run python -m app.main score-candidates

Com limite:

    uv run python -m app.main score-candidates --limit 100

Forcando recalculo:

    uv run python -m app.main score-candidates --limit 100 --force

Com output em portugues sem acentos:

    uv run python -m app.main score-candidates --limit 100 --language pt-BR

### 6. Ranqueiar oportunidades

    uv run python -m app.main rank-opportunities

Com limite:

    uv run python -m app.main rank-opportunities --limit 20

Filtrando por score minimo:

    uv run python -m app.main rank-opportunities --min-final-score 0.7

Filtrando por nivel de confianca:

    uv run python -m app.main rank-opportunities --confidence-level high

Filtrando por categorias com anuncio permitido:

    uv run python -m app.main rank-opportunities --listing-allowed true

Filtrando por tamanho maximo da categoria:

    uv run python -m app.main rank-opportunities --max-category-total-items 10000

Com output em portugues sem acentos:

    uv run python -m app.main rank-opportunities --language pt-BR --limit 20

### 7. Gerar alertas

    uv run python -m app.main alert-opportunities

Com limite:

    uv run python -m app.main alert-opportunities --limit 50

Com output em portugues sem acentos:

    uv run python -m app.main alert-opportunities --limit 50 --language pt-BR

### 8. Listar alertas

    uv run python -m app.main list-alerts

Com limite:

    uv run python -m app.main list-alerts --limit 50

Filtrando por status:

    uv run python -m app.main list-alerts --status open

Filtrando por score minimo:

    uv run python -m app.main list-alerts --min-final-score 0.7

Filtrando por nivel de confianca:

    uv run python -m app.main list-alerts --confidence-level high

Com output em portugues sem acentos:

    uv run python -m app.main list-alerts --language pt-BR --limit 50

### 9. Gerar analises comerciais

    uv run python -m app.main commercial-opportunities

Com limite:

    uv run python -m app.main commercial-opportunities --limit 20

Com output em portugues sem acentos:

    uv run python -m app.main commercial-opportunities --limit 20 --language pt-BR

### 10. Listar analises comerciais

    uv run python -m app.main list-commercial-analyses

Com limite:

    uv run python -m app.main list-commercial-analyses --limit 20

Filtrando por decisao comercial:

    uv run python -m app.main list-commercial-analyses --commercial-decision dropshipping_candidate

    uv run python -m app.main list-commercial-analyses --commercial-decision affiliate_candidate

    uv run python -m app.main list-commercial-analyses --commercial-decision research_needed

    uv run python -m app.main list-commercial-analyses --commercial-decision avoid

Filtrando por risco:

    uv run python -m app.main list-commercial-analyses --risk-level low

    uv run python -m app.main list-commercial-analyses --risk-level medium

    uv run python -m app.main list-commercial-analyses --risk-level high

Filtrando por score comercial minimo:

    uv run python -m app.main list-commercial-analyses --min-commercial-score 0.7

Combinando filtros:

    uv run python -m app.main list-commercial-analyses --commercial-decision affiliate_candidate --risk-level low --min-commercial-score 0.65

Com output em portugues sem acentos:

    uv run python -m app.main list-commercial-analyses --language pt-BR --limit 20

---

## Execucao recomendada completa

Para rodar o pipeline principal em sequencia:

    uv run python -m app.main sync-trends
    uv run python -m app.main build-candidates
    uv run python -m app.main qualify-candidates
    uv run python -m app.main enrich-candidates --limit 20
    uv run python -m app.main score-candidates
    uv run python -m app.main rank-opportunities
    uv run python -m app.main alert-opportunities
    uv run python -m app.main commercial-opportunities
    uv run python -m app.main list-commercial-analyses

Com outputs em portugues sem acentos nas etapas de leitura:

    uv run python -m app.main rank-opportunities --language pt-BR
    uv run python -m app.main list-alerts --language pt-BR
    uv run python -m app.main commercial-opportunities --language pt-BR
    uv run python -m app.main list-commercial-analyses --language pt-BR

---

## Commercial Intelligence Layer

A camada de inteligencia comercial transforma oportunidades tecnicas em decisoes mais proximas de acao comercial.

Ela reaproveita o ranking estrutural gerado pelo pipeline e classifica cada oportunidade em uma das seguintes decisoes:

- `dropshipping_candidate`: oportunidade com sinais suficientes para validar fornecedor, frete, taxas e margem.
- `affiliate_candidate`: oportunidade indicada para validacao com afiliados ou conteudo antes de exposicao operacional.
- `research_needed`: oportunidade promissora, mas ainda dependente de dados adicionais.
- `avoid`: oportunidade que nao deve ser priorizada no momento.

A analise comercial considera:

- score estrutural da oportunidade;
- qualidade da predicao;
- risco operacional;
- complexidade da categoria;
- quantidade de atributos obrigatorios;
- sinais heuristicos de preco;
- dados ausentes necessarios para validacao comercial.

As analises comerciais sao persistidas em `commercial_opportunity_analysis`, permitindo historico e comparacao futura.

---

## Localized outputs

A CLI suporta outputs JSON localizados para comandos que retornam dados estruturados.

O codigo interno, os valores persistidos e os identificadores de dominio permanecem em ingles. A camada de apresentacao pode traduzir nomes de campos e valores selecionados no momento do output.

Idiomas suportados:

- `en`: output padrao em ingles.
- `pt-BR`: output em portugues sem acentos, adequado para reports, exports CSV e integracoes externas.

Exemplos:

    uv run python -m app.main list-commercial-analyses --language pt-BR --limit 5
    uv run python -m app.main commercial-opportunities --language pt-BR --limit 5
    uv run python -m app.main rank-opportunities --language pt-BR --limit 5

O output em portugues evita acentos intencionalmente para reduzir problemas de compatibilidade em reports gerados, exports CSV e integracoes externas.

---

## Autenticacao Mercado Livre

### Trocar authorization code por token

    uv run python -m app.main auth-bootstrap "<authorization_code>"

### Ler usuario atual

    uv run python -m app.main auth-current-user

Com output em portugues sem acentos:

    uv run python -m app.main auth-current-user --language pt-BR

### Forcar refresh do token

    uv run python -m app.main auth-refresh

---

## Git e branches

### Ver branch atual

    git branch --show-current

### Ver status

    git status

### Atualizar master

    git checkout master
    git pull origin master

### Criar branch nova

    git checkout -b feat/nome-da-feature

### Adicionar arquivos

    git add .

### Commit de feature

    git commit -m "feat: descricao objetiva da entrega"

### Commit de correcao

    git commit -m "fix: descricao objetiva da correcao"

### Commit de documentacao

    git commit -m "docs: descricao objetiva da documentacao"

### Merge local na master

    git checkout master
    git pull origin master
    git merge nome-da-branch

### Push

    git push origin master

---

## Commits recentes sugeridos neste ciclo

Camada comercial:

    git commit -m "feat: add commercial opportunity analysis layer"

Persistencia da analise comercial:

    git commit -m "feat: persist commercial opportunity analysis"

Listagem de analises comerciais:

    git commit -m "feat: add commercial analysis listing command"

Presenter global localizado:

    git commit -m "feat: add global localized output presenter"

Remocao de acentos do output localizado:

    git commit -m "fix: remove accents from localized output"

Documentacao dos outputs localizados:

    git commit -m "docs: document localized CLI outputs"

Referencia completa de comandos:

    git commit -m "docs: expand README command reference"

---

## Troubleshooting

### Erro: Failed to spawn `app`

Se este comando falhar:

    uv run app rank-opportunities

Use o modulo Python diretamente:

    uv run python -m app.main rank-opportunities

### Erro: Can't locate revision identified by alguma revision

Verifique o head reconhecido pelos arquivos:

    uv run alembic heads

Verifique a revision registrada no banco:

    psql "postgresql://postgres:postgres@localhost:5432/mercadolivre_ml" -c "select * from alembic_version;"

Se o banco estiver apontando para uma revision que nao existe mais nos arquivos, ajuste manualmente com cuidado:

    psql "postgresql://postgres:postgres@localhost:5432/mercadolivre_ml" -c "update alembic_version set version_num = '<revision_valida_anterior>';"

Depois rode:

    uv run alembic upgrade head

### Erro de senha no psql

Se o comando abaixo pedir senha para o usuario errado:

    psql "$env:DATABASE_URL"

Use a URL explicita do banco:

    psql "postgresql://postgres:postgres@localhost:5432/mercadolivre_ml"

### URL do SQLAlchemy nao funciona no psql

A aplicacao pode usar:

    DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/mercadolivre_ml

Mas o `psql` deve usar:

    postgresql://postgres:postgres@localhost:5432/mercadolivre_ml

---

## Observacoes importantes

- O projeto ainda nao calcula margem real com base em fornecedores, taxas e frete.
- A camada comercial atual usa sinais estruturais e heuristicas iniciais.
- Dados reais de preco, concorrencia e margem continuam sendo a proxima fronteira para aumentar a precisao comercial.
- O endpoint publico de search do Mercado Livre apresentou bloqueio no ambiente atual.
- O projeto deve continuar evoluindo de forma incremental, com branches pequenas e commits rastreaveis.
- Os outputs em `pt-BR` devem permanecer sem acentos por decisao de compatibilidade.
