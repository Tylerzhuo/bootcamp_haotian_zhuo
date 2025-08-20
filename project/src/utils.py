from __future__ import annotations
import re
import pandas as pd
import numpy as np

def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert column names to snake_case and strip whitespace.
    - spaces/dashes -> underscore
    - remove non-alnum/underscore
    - collapse repeated underscores
    """
    def _clean(s: str) -> str:
        s = s.strip()
        s = re.sub(r"[\s\-]+", "_", s)
        s = re.sub(r"[^0-9a-zA-Z_]", "", s)
        s = re.sub(r"_+", "_", s)
        return s.lower().strip("_")
    out = df.copy()
    out.columns = [_clean(c) for c in out.columns]
    return out


def get_summary_stats(df):
    return df.describe()