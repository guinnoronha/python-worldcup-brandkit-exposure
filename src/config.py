from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"
DASHBOARDS = PROJECT_ROOT / "dashboards"

INPUT_XLSX = DATA_RAW / "worldcup_info.xlsx"

CSV_SEP = ","
CSV_ENCODING = "utf-8"