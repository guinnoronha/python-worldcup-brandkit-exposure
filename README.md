# World Cup Kit Suppliers — Exposição de Marcas vs Performance (1970–2022)

Projeto de engenharia de dados em Python para analisar a relação entre a **exposição de marcas fornecedoras de material esportivo** (quais e quantas seleções cada marca vestiu em cada Copa) e a **performance esportiva dessas seleções** (posição final, fase alcançada, campeão, top-4, top-8).

Cobre **14 edições** da Copa do Mundo FIFA (1970–2022), **368 registros** seleção-ano e **47 marcas** distintas.

---

## Estrutura do projeto

```
worldcup-kit-exposure/
├── data/
│   ├── raw/
│   │   └── worldcup_info.xlsx          # Fonte de dados bruta (3 abas)
│   └── processed/
│       ├── fact_team_tournament.csv    # Fato: seleção-ano (368 linhas)
│       ├── brand_tournament_summary.csv # Agregado: marca por copa (122 linhas)
│       └── brand_overall_summary.csv   # Agregado: marca geral (47 linhas)
├── dashboards/
│   └── brand_exposure_dashboard.html   # Dashboard de resultados
├── src/
│   ├── config.py      # Caminhos do projeto
│   ├── io.py          # Leitura do Excel
│   ├── transform.py   # Limpeza e construção da tabela fato
│   ├── metrics.py     # Agregações por marca
│   ├── dashboard.py   # Geração do dashboard 
│   └── pipeline.py    # Orquestrador: executa o pipeline completo
├── notebooks/
├── requirements.txt
└── README.md
```

---

## Dados brutos

**Arquivo:** `data/raw/worldcup_info.xlsx`

| Aba | Descrição | Colunas principais |
|-----|-----------|-------------------|
| `results` | Resultado de cada seleção em cada Copa | `year`, `team_qid`, `team_name`, `final_position`, `stage_reached` |
| `worldcup_info` | Metadados das edições da Copa | — |
| `team_kit_supplier` | Fornecedor de uniforme por seleção e Copa | `year`, `team_qid`, `team_name`, `brand_name`, `brand_name_normalized` |

---

## Camada processada

### `fact_team_tournament.csv` — seleção × copa

| Coluna | Tipo | Descrição |
|--------|------|-----------|
| `year` | int | Ano da Copa |
| `team_qid` | str | ID Wikidata da seleção |
| `team_name` | str | Nome da seleção |
| `final_position` | int | Colocação final (1 = campeão) |
| `stage_reached` | str | Fase alcançada |
| `brand` | str | Marca normalizada (minúsculo) |
| `brand_name` | str | Nome oficial da marca |
| `has_brand` | bool | Se há dado de marca disponível |
| `is_champion` | bool | Campeão da edição |
| `is_runner_up` | bool | Vice-campeão |
| `is_top4` | bool | Top-4 |
| `is_top8` | bool | Top-8 |
| `is_top16` | bool | Top-16 |
| `stage_norm` | str | Fase normalizada |

### `brand_tournament_summary.csv` — marca × copa

Colunas-chave: `teams`, `champions`, `top4`, `top8`, `top16`, `avg_final_position`, `share_teams`, `share_champions`, `share_top4`, `share_top8`.

### `brand_overall_summary.csv` — marca (todas as copas)

Colunas-chave: `exposures`, `unique_teams`, `tournaments`, `champions`, `top4`, `top8`, `avg_final_position`, `champion_rate_per_exposure`, `top4_rate_per_exposure`, `top8_rate_per_exposure`.

---

## Pipeline (`src/`)

| Módulo | Responsabilidade |
|--------|-----------------|
| `config.py` | Define os caminhos (`DATA_RAW`, `DATA_PROCESSED`, `DASHBOARDS`) |
| `io.py` | Lê as três abas do Excel |
| `transform.py` | Limpa os dados, faz o join resultados + fornecedores e calcula os buckets de performance |
| `metrics.py` | Gera os dois CSVs de agregação |
| `dashboard.py` | Gera `worldcup_brands_dashboard.html` com Plotly |
| `pipeline.py` | Orquestra tudo: leitura → transformação → métricas → CSV → dashboard |

### Executar o pipeline

```bash
# 1. Criar e ativar o ambiente virtual
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Rodar o pipeline
python -m src.pipeline
```

Os CSVs processados e o `worldcup_brands_dashboard.html` serão criados/atualizados automaticamente.

---

## Dashboards

### `worldcup_brands_dashboard.html` (Plotly — gerado pelo pipeline)

Gerado automaticamente ao rodar `src/pipeline.py`. Contém quatro visualizações interativas:

- Evolução do share de seleções por marca ao longo das Copas (área empilhada)
- Número de títulos por marca (barras)
- Eficiência: taxa de título por exposição vs total de exposições (scatter)
- Tabela resumo das top-20 marcas

### `brand_exposure_dashboard.html` (Chart.js — estático, tema escuro)

Dashboard standalone — basta abrir no browser, sem dependência de servidor. Inclui:

- KPIs globais (títulos por marca, melhor taxa de eficiência, maior share de uma edição)
- Stacked bar: número de seleções por marca em cada Copa (1970–2022)
- Barras horizontais: taxa de título, top-4 e top-8 por marca
- Donut: distribuição de marcas na Copa de 2022
- Linha temporal: evolução de share Adidas vs Nike (com pontos dourados marcando copas vencidas)
- Bubble charts: exposições × taxa de título e posição média × exposições
- Tabela completa do pódio (Top-4) por edição com brand chips
- Ranking consolidado de todas as marcas com mini-barras de performance

---

## Principais achados

| Marca | Exposições | Títulos | Taxa de título | Top-4 |
|-------|-----------|---------|---------------|-------|
| Adidas | 124 | 6 | 4,8% | 24 |
| Nike | 66 | 2 | 3,0% | 14 |
| Puma | 46 | 1 | 2,2% | 3 |
| Umbro | 32 | 1 | 3,1% | 3 |
| Le Coq Sportif | 9 | 2 | **22,2%** | 2 |

- **Adidas** dominou em volume absoluto: vestiu entre 37% e 62% das seleções por Copa entre 1974 e 1990.
- **Nike** entrou apenas a partir de 1998 e chegou a 40,6% de share em 2022 (13 de 32 seleções).
- **Le Coq Sportif** tem a maior taxa de título por exposição (22,2%): venceu com Argentina (1986) e Itália (1982).
- A Copa de 1978 é a única com 3 seleções do pódio (Top-3) vestindo a mesma marca (Adidas).

---

## Dependências

```
pandas>=2.0
openpyxl>=3.1
plotly>=5.18
numpy>=1.24
```

---

## Criado por

**Guilherme Noronha Mello**<br>
**Linkedin:** linkedin.com/in/guilherme-noronha-mello/<br>
**Github:** github.com/guinnoronha
