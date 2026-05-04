from pathlib import Path
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def build_dashboard_html(
    fact: pd.DataFrame,
    brand_year: pd.DataFrame,
    brand_overall: pd.DataFrame,
    out_path: Path
):
    out_path.parent.mkdir(parents=True, exist_ok=True)

    bo = brand_overall.dropna(subset=["brand"]).copy()
    bo = bo[bo["brand"].astype(str).str.len() > 0].copy()

    top_brands = bo.head(10)["brand"].tolist()
    by = brand_year[brand_year["brand"].isin(top_brands)].copy().sort_values("year")

    fig1 = px.area(
        by,
        x="year",
        y="share_teams",
        color="brand",
        title="Exposição por marca (share de seleções por Copa) — Top 10 marcas",
        labels={"share_teams": "Share de seleções", "year": "Ano", "brand": "Marca"},
    )

    fig2 = px.bar(
        bo.head(15),
        x="brand",
        y="champions",
        title="Número de títulos (campeões) por marca — Top 15",
        labels={"brand": "Marca", "champions": "Títulos"},
    )
    fig2.update_layout(xaxis_tickangle=-45)

    fig3 = px.scatter(
        bo,
        x="exposures",
        y="champion_rate_per_exposure",
        size="champions",
        color="brand",
        hover_data=["top4", "top8", "avg_final_position", "tournaments"],
        title="Eficiência: títulos/exposição vs total de exposições",
        labels={"exposures": "Exposições (team-year)", "champion_rate_per_exposure": "Títulos / exposição"},
    )

    table = bo.head(20).copy()
    fig4 = go.Figure(
        data=[go.Table(
            header=dict(values=list(table.columns)),
            cells=dict(values=[table[c].tolist() for c in table.columns]),
        )]
    )
    fig4.update_layout(title="Resumo geral (Top 20 marcas)")

    html = f"""
    <html>
    <head>
      <meta charset="utf-8"/>
      <title>World Cup Kit Suppliers — Exposição vs Performance</title>
      <style>
        body {{ font-family: Arial, sans-serif; margin: 24px; }}
        h1 {{ margin-bottom: 6px; }}
        p {{ margin-top: 0; color: #444; }}
      </style>
    </head>
    <body>
      <h1>World Cup Kit Suppliers — Exposição vs Performance (1970–2022)</h1>
      <p>Dashboard gerado com pandas + plotly.</p>
      {fig1.to_html(full_html=False, include_plotlyjs="cdn")}
      {fig2.to_html(full_html=False, include_plotlyjs=False)}
      {fig3.to_html(full_html=False, include_plotlyjs=False)}
      {fig4.to_html(full_html=False, include_plotlyjs=False)}
    </body>
    </html>
    """

    out_path.write_text(html, encoding="utf-8")