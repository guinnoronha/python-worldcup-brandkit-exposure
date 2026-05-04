import pandas as pd

def brand_tournament_summary(fact: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega por (year, brand):
    - teams: nº de seleções com a marca naquele ano
    - champions/top4/top8/top16: contagens
    - shares dentro do ano (ex.: share_teams)
    """
    df = fact.copy()

    out = (
        df.groupby(["year", "brand"], dropna=False)
          .agg(
              teams=("team_qid", "nunique"),
              champions=("is_champion", "sum"),
              top4=("is_top4", "sum"),
              top8=("is_top8", "sum"),
              top16=("is_top16", "sum"),
              avg_final_position=("final_position", "mean"),
              median_final_position=("final_position", "median"),
              teams_with_position=("final_position", lambda s: s.notna().sum()),
          )
          .reset_index()
    )

    year_totals = (
        out.groupby("year", as_index=False)
           .agg(
               total_teams=("teams", "sum"),
               total_champions=("champions", "sum"),
               total_top4=("top4", "sum"),
               total_top8=("top8", "sum"),
               total_top16=("top16", "sum"),
           )
    )
    out = out.merge(year_totals, on="year", how="left")

    for col, tot in [
        ("teams", "total_teams"),
        ("champions", "total_champions"),
        ("top4", "total_top4"),
        ("top8", "total_top8"),
        ("top16", "total_top16"),
    ]:
        out[f"share_{col}"] = out[col] / out[tot]

    return out


def brand_overall_summary(fact: pd.DataFrame) -> pd.DataFrame:
    """
    Agrega por brand (todas as copas):
    - exposures: total de aparições (team-year)
    - champions/top4/top8
    - taxas por exposição
    """
    df = fact.copy()
    df["exposures"] = 1

    out = (
        df.groupby("brand", dropna=False)
          .agg(
              exposures=("exposures", "sum"),
              unique_teams=("team_qid", "nunique"),
              tournaments=("year", "nunique"),
              champions=("is_champion", "sum"),
              top4=("is_top4", "sum"),
              top8=("is_top8", "sum"),
              avg_final_position=("final_position", "mean"),
              median_final_position=("final_position", "median"),
          )
          .reset_index()
    )

    out["champion_rate_per_exposure"] = out["champions"] / out["exposures"]
    out["top4_rate_per_exposure"] = out["top4"] / out["exposures"]
    out["top8_rate_per_exposure"] = out["top8"] / out["exposures"]

    return out.sort_values(["champions", "top4", "exposures"], ascending=False)