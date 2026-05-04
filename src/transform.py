import pandas as pd

def _clean_str(s: pd.Series) -> pd.Series:
    return (
        s.astype("string")
         .str.strip()
         .str.replace(r"\s+", " ", regex=True)
    )

def clean_inputs(results, worldcup_info, team_kit_supplier):
    results = results.copy()
    worldcup_info = worldcup_info.copy()
    team_kit_supplier = team_kit_supplier.copy()

    for df in (results, worldcup_info, team_kit_supplier):
        if "year" in df.columns:
            df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")

    if "team_name" in results.columns:
        results["team_name"] = _clean_str(results["team_name"])
    if "team_name" in team_kit_supplier.columns:
        team_kit_supplier["team_name"] = _clean_str(team_kit_supplier["team_name"])

    # Marca normalizada
    if "brand_name_normalized" in team_kit_supplier.columns:
        team_kit_supplier["brand"] = _clean_str(team_kit_supplier["brand_name_normalized"]).str.lower()
    else:
        team_kit_supplier["brand"] = _clean_str(team_kit_supplier["brand_name"]).str.lower()

    # Garantir colunas esperadas existam (para evitar KeyError)
    for col in ["brand_name", "brand_name_normalized"]:
        if col not in team_kit_supplier.columns:
            team_kit_supplier[col] = pd.NA

    return results, worldcup_info, team_kit_supplier


def build_fact_team_tournament(results, team_kit_supplier):
    """
    Grão: (year, team_qid) — uma linha por seleção em cada Copa,
    com desempenho + marca do uniforme.
    """
    r = results.copy()
    k = team_kit_supplier.copy()

    key = ["year", "team_qid"]

    fact = r.merge(
        k[key + ["brand", "brand_name", "brand_name_normalized", "team_name"]],
        on=key,
        how="left",
        suffixes=("", "_kit"),
    )

    # resolve team_name final
    if "team_name_kit" in fact.columns:
        fact["team_name"] = fact["team_name"].fillna(fact["team_name_kit"])
        fact = fact.drop(columns=["team_name_kit"])

    fact["has_brand"] = fact["brand"].notna()

    if "final_position" in fact.columns:
        fact["final_position"] = pd.to_numeric(fact["final_position"], errors="coerce").astype("Int64")
    else:
        fact["final_position"] = pd.NA

    if "stage_reached" not in fact.columns:
        fact["stage_reached"] = pd.NA

    return fact


def add_performance_buckets(fact: pd.DataFrame) -> pd.DataFrame:
    """
    Buckets de performance baseados principalmente em final_position.
    Se final_position estiver ausente, tenta inferir algo via stage_reached (heurístico).
    """
    df = fact.copy()
    pos = df["final_position"]

    df["is_champion"] = (pos == 1)
    df["is_runner_up"] = (pos == 2)
    df["is_top4"] = pos.isin([1, 2, 3, 4])
    df["is_top8"] = pos.notna() & pos.between(1, 8)
    df["is_top16"] = pos.notna() & pos.between(1, 16)

    stage = df["stage_reached"].astype("string").str.lower()
    df["stage_norm"] = stage

    missing_pos = pos.isna()

    # heurísticas (ajuste se seus valores forem diferentes)
    df.loc[missing_pos, "is_champion"] = stage.str.contains("winner|champion|campe", regex=True, na=False)
    df.loc[missing_pos, "is_top4"] = stage.str.contains("semi|3rd|third|fourth|4th|semif", regex=True, na=False)
    df.loc[missing_pos, "is_top8"] = (
        stage.str.contains("quarter|quart|qf", regex=True, na=False)
        | df.loc[missing_pos, "is_top4"]
    )
    df.loc[missing_pos, "is_top16"] = (
        stage.str.contains("round of 16|oitavas|r16", regex=True, na=False)
        | df.loc[missing_pos, "is_top8"]
    )

    return df