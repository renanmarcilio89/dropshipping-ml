# Mercado Livre ML Pipeline

Scaffolding inicial para um pipeline modular de inteligência de mercado no Mercado Livre, orientado a:

- descoberta de demanda
- coleta de resultados de busca
- enriquecimento de itens
- normalização de concorrência
- cálculo de score de oportunidade
- alertas

## Stack

- Python 3.12
- SQLAlchemy 2.x
- Alembic
- PostgreSQL
- httpx
- Pydantic v2
- Typer
- structlog
- pytest

## Contas, credenciais e possíveis custos

### 1. Mercado Livre Developers
Necessário criar uma aplicação no portal Developers para obter credenciais OAuth e access token. A documentação oficial informa que o token deve ser enviado no header de autorização em todas as chamadas e que a aplicação pode atuar em nome do usuário enquanto o token estiver válido. citeturn714139search0turn714139search13

Impacto de custo: normalmente não há custo direto para criar a aplicação, mas existe custo indireto de desenvolvimento, manutenção e eventual infraestrutura de execução.

### 2. Banco PostgreSQL
Você pode rodar localmente sem custo inicial. Se optar por serviço gerenciado, haverá custo mensal.

### 3. Scheduler / worker
Nesta fase o projeto nasce com CLI e jobs sincronizáveis por cron/Task Scheduler. Isso evita custo inicial com Celery broker, filas gerenciadas ou orquestradores pagos.

## Boas práticas importantes

A documentação do Mercado Livre recomenda trabalhar com a API em vez de web crawling. Nosso desenho segue essa diretriz: API-first e scraping HTML apenas como complemento pontual, quando estritamente necessário. citeturn714139search7

## Checkpoints de commit sugeridos

1. `chore: bootstrap do projeto e configuração base`
2. `feat: cliente Mercado Livre e schemas iniciais`
3. `feat: models SQLAlchemy e sessão de banco`
4. `feat: jobs de trends, search e enrich`
5. `feat: score de oportunidade e alertas`
6. `test: cobertura inicial do core e scoring`

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate  # Windows
pip install -e .[dev]
```

## Variáveis de ambiente

Copie `.env.example` para `.env` e preencha os valores.

## CLI

```bash
ml-pipeline health
ml-pipeline sync-trends
ml-pipeline search-marketplace --query "garrafa termica"
```
