import pandas as pd
from .config import INPUT_XLSX

def read_input_excel(path=INPUT_XLSX):
    # nomes exatos das abas do seu arquivo
    results = pd.read_excel(path, sheet_name="results")
    worldcup_info = pd.read_excel(path, sheet_name="worldcup_info")
    team_kit_supplier = pd.read_excel(path, sheet_name="team_kit_supplier")
    return results, worldcup_info, team_kit_supplier