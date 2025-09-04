import pandas as pd
from pathlib import Path

def load_crops(csv_path: str):
    p = Path(csv_path)
    if not p.exists():
        return pd.DataFrame()
    return pd.read_csv(p)
