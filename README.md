# G1 Pulse — Analytics de Conteúdo Editorial

> Projeto de portfólio inspirado no ciclo analítico de produtos de notícias digitais (G1/Globo), construído para praticar SQL avançado, BigQuery, testes A/B e dashboards executivos em escala de portfólio Jr.

## Contexto

Este projeto simula, em escala reduzida, o ciclo analítico descrito por times de dados de produtos de notícia digital: extração de dados editoriais, modelagem em data warehouse, testes A/B e dashboards de engajamento.

Foi criado como projeto de estudo/portfólio para candidatura a vaga de Analista de Dados Jr. **Não possui nenhum vínculo, acesso ou afiliação com a Globo/G1.**

## ⚠️ Transparência sobre os dados

| Camada | Origem | Tipo |
|---|---|---|
| Metadados editoriais (título, editoria, data/hora de publicação) | Feeds RSS públicos do G1 (`g1.globo.com/rss/g1/<editoria>`) | **Real** |
| Métricas de engajamento (pageviews, tempo na página, compartilhamentos) | Geradas por modelo estatístico próprio, calibrado com padrões públicos e genéricos do setor de mídia digital | **Simulado** |
| Teste A/B de manchete | Variantes e taxas de conversão definidas manualmente para fins de demonstração | **Simulado** |

Detalhamento completo de premissas e limitações em [`docs/metodologia.md`](docs/metodologia.md). Isso é mencionado de forma explícita porque métricas de audiência de produtos de mídia são dados proprietários — a honestidade sobre o que é real e o que é simulado é parte do propósito do projeto.

## Stack

- **Coleta:** Python (`requests`, `feedparser`)
- **Automação:** GitHub Actions (coleta agendada)
- **Processamento:** Python (`pandas`, `numpy`)
- **Data Warehouse:** Google BigQuery (free tier)
- **Análise estatística:** `scipy` / `statsmodels` (teste A/B)
- **Dashboards:** Looker Studio + Power BI

## Estrutura do repositório

```
g1-pulse-analytics/
├── .github/workflows/      # CI: coleta automática de RSS
├── data/
│   ├── raw/                # camada real (RSS coletado)
│   └── processed/          # camada real + engajamento simulado
├── docs/
│   └── metodologia.md      # transparência sobre dados reais vs. simulados
├── notebooks/              # exploração e EDA
├── sql/queries/            # queries de análise no BigQuery
├── src/
│   ├── collect/            # coleta dos feeds RSS
│   ├── synthetic/          # geração da camada de engajamento simulado
│   ├── etl/                # carga no BigQuery
│   └── analysis/           # teste A/B
└── dashboards/             # links/arquivos dos dashboards
```

## Como rodar

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Coletar dados reais (RSS do G1)
python src/collect/rss_collector.py

# 3. Gerar camada de engajamento simulado
python src/synthetic/generate_engagement.py

# 4. (Opcional) Carregar no BigQuery — requer .env configurado
cp .env.example .env  # preencher com suas credenciais GCP
python src/etl/bigquery_loader.py

# 5. Simular e analisar teste A/B
python src/analysis/ab_test.py
```

## Status do projeto

- [x] Estrutura do repositório
- [ ] Coleta de dados RSS rodando via GitHub Actions
- [ ] Geração da camada sintética
- [ ] Carga no BigQuery
- [ ] Queries SQL de análise
- [ ] Teste A/B
- [ ] Dashboard Looker Studio
- [ ] Dashboard Power BI

## Autor

Lucas Busquet de Azevedo — [LinkedIn](https://www.linkedin.com/in/lucas-busquet) · [GitHub](https://github.com/lucasbusquetazevedo)
