from sklearn.preprocessing import MinMaxScaler, StandardScaler
import pandas as pd
import numpy as np

def load_raw(symbol: str, raw_path: str = "data/raw") -> pd.DataFrame:
    """Load raw CSV for given ticker into a DataFrame."""
    path = f"{raw_path}/{symbol}_daily.csv"
    df = pd.read_csv(path, parse_dates=[0], index_col=0)
    df["symbol"] = symbol
    return df

def fill_missing_median(df, columns=None):
    df_copy = df.copy()
    if columns is None:
        columns = df.select_dtypes(include=np.number).columns
    for col in columns:
        df_copy[col] = df_copy[col].fillna(df_copy[col].median())
    return df_copy

def drop_missing(df, columns=None, threshold=None):
    df_copy = df.copy()
    if columns is not None:
        return df_copy.dropna(subset=columns)
    if threshold is not None:
        return df_copy.dropna(thresh=int(threshold*df_copy.shape[1]))
    return df_copy.dropna()

def normalize_data(df, columns=None, method='minmax'):
    df_copy = df.copy()
    if columns is None:
        columns = df_copy.select_dtypes(include=np.number).columns
    if method=='minmax':
        scaler = MinMaxScaler()
    else:
        scaler = StandardScaler()
    df_copy[columns] = scaler.fit_transform(df_copy[columns])
    return df_copy

def correct_column_types(df):
    df_copy = df.copy()
    if 'price' in df_copy.columns:
        df_copy['price'] = df_copy['price'].str.replace('$','').astype(float)
    if 'date_str' in df_copy.columns:
        df_copy['date'] = pd.to_datetime(df_copy['date_str'], errors='coerce')
    if 'category' in df_copy.columns:
        df_copy['category'] = df_copy['category'].str.lower().astype('category')
    return df_copy

def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names (shorter and consistent).
    Adjusts whether data is adjusted schema or daily schema.
    """
    mapping_adj = {
        "1. open": "open",
        "2. high": "high",
        "3. low": "low",
        "4. close": "close",
        "5. adjusted close": "adj_close",
        "6. volume": "volume",
        "7. dividend amount": "dividend",
        "8. split coefficient": "split_coeff",
    }
    mapping_daily = {
        "1. open": "open",
        "2. high": "high",
        "3. low": "low",
        "4. close": "close",
        "5. volume": "volume",
    }
    if "5. adjusted close" in df.columns:
        return df.rename(columns=mapping_adj)
    else:
        return df.rename(columns=mapping_daily)

def enforce_types(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure numeric columns are correct dtypes."""
    numeric_cols = [c for c in df.columns if c not in ["symbol"]]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")
    return df

def preprocess(symbol: str, raw_path="../data/raw", out_path="../data/processed") -> pd.DataFrame:
    """Full preprocessing pipeline for one ticker."""
    df = load_raw(symbol, raw_path)
    df = drop_missing(df)
    df = rename_columns(df)
    df = enforce_types(df)
    # Save processed file
    out_file = f"{out_path}/{symbol}_clean.csv"
    df.to_csv(out_file)
    print(f"Saved cleaned data for {symbol} → {out_file}")
    return df