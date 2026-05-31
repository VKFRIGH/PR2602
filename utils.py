from pathlib import Path
from typing import Optional

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

DATA_DIR = Path(__file__).parent
DEFAULT_QOL_FILE = DATA_DIR / "data" / "quality_of_life_indices_by_country.csv"


def _normalize_country_column(df: pd.DataFrame) -> pd.DataFrame:
    if "Country Name" in df.columns and "Country" not in df.columns:
        df = df.rename(columns={"Country Name": "Country"})
    return df


def _read_csv_payload(file_path: Path, chunksize: int) -> pd.DataFrame:
    if chunksize and chunksize > 0:
        chunks = []
        for chunk in pd.read_csv(file_path, chunksize=chunksize):
            chunks.append(chunk)
        return pd.concat(chunks, ignore_index=True)
    return pd.read_csv(file_path)


def load_data(file_path: Optional[Path] = None, chunksize: int = 0) -> pd.DataFrame:
    if file_path is None:
        file_path = DEFAULT_QOL_FILE

    df = _read_csv_payload(file_path, chunksize)
    df = _normalize_country_column(df)
    if "Year" in df.columns:
        df["Year"] = df["Year"].astype(str).str.replace(r"/2$", "", regex=True).astype(int)
    return df


def load_time_series_data(file_path: Optional[Path] = None, chunksize: int = 0) -> pd.DataFrame:
    df = load_data(file_path=file_path, chunksize=chunksize)
    if "Country" in df.columns and "Year" in df.columns:
        df = df.groupby(["Country", "Year"], as_index=False, sort=False).mean(numeric_only=True)
    return df


def get_growth_by_period(df: pd.DataFrame, start_year: int, end_year: int) -> pd.DataFrame:
    pivot = df.pivot_table(index="Country", columns="Year", values="Quality of Life Index")
    if start_year not in pivot.columns or end_year not in pivot.columns:
        raise ValueError("Izbrano obdobje ni na voljo v podatkih.")
    growth_df = pd.DataFrame(pivot[end_year] - pivot[start_year], columns=["Net_Growth"]).dropna()
    growth_df.index.name = "Country"
    return growth_df


def cluster_growth(df_growth: pd.DataFrame, n_clusters: int = 3, random_state: int = 42) -> pd.DataFrame:
    df = df_growth.copy()
    scaler = StandardScaler()
    scaled = scaler.fit_transform(df[["Net_Growth"]])
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
    df["Cluster"] = kmeans.fit_predict(scaled)
    return df


def standardize_features(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    return (df[cols] - df[cols].mean()) / df[cols].std()
