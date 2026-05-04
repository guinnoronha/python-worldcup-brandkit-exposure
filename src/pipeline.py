from .config import DATA_PROCESSED, DASHBOARDS, CSV_SEP, CSV_ENCODING
from .io import read_input_excel
from .transform import clean_inputs, build_fact_team_tournament, add_performance_buckets
from .metrics import brand_tournament_summary, brand_overall_summary
from .dashboard import build_dashboard_html

def run():
    DATA_PROCESSED.mkdir(parents=True, exist_ok=True)
    DASHBOARDS.mkdir(parents=True, exist_ok=True)

    results, worldcup_info, team_kit_supplier = read_input_excel()
    results, worldcup_info, team_kit_supplier = clean_inputs(results, worldcup_info, team_kit_supplier)

    fact = build_fact_team_tournament(results, team_kit_supplier)
    fact = add_performance_buckets(fact)

    brand_year = brand_tournament_summary(fact)
    brand_overall = brand_overall_summary(fact)

    # CSV outputs
    fact.to_csv(
        DATA_PROCESSED / "fact_team_tournament.csv",
        index=False,
        sep=CSV_SEP,
        encoding=CSV_ENCODING
    )
    brand_year.to_csv(
        DATA_PROCESSED / "brand_tournament_summary.csv",
        index=False,
        sep=CSV_SEP,
        encoding=CSV_ENCODING
    )
    brand_overall.to_csv(
        DATA_PROCESSED / "brand_overall_summary.csv",
        index=False,
        sep=CSV_SEP,
        encoding=CSV_ENCODING
    )

    # Dashboard
    build_dashboard_html(
        fact=fact,
        brand_year=brand_year,
        brand_overall=brand_overall,
        out_path=DASHBOARDS / "worldcup_brands_dashboard.html"
    )

if __name__ == "__main__":
    run()