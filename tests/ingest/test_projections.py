from pathlib import Path

import polars as pl

from ffa.ingest.projections import read_projections


DATA_DIR = Path(__file__).parent / "data"


def _check_df(df: pl.DataFrame) -> None:
    assert df.columns == ["player_id", "name", "team", "position", "week", "points"]
    assert df.height == 6

    alice = df.filter(pl.col("name") == "Alice").sort("week")
    assert alice.select("points").to_series().to_list() == [10.0, 0.0, 5.0]

    bob = df.filter(pl.col("name") == "Bob").sort("week")
    assert bob.select("points").to_series().to_list() == [8.0, 0.0, 0.0]

    assert alice.select("player_id").n_unique() == 1
    assert bob.select("player_id").n_unique() == 1
    assert alice.select("player_id").to_series()[0] != bob.select("player_id").to_series()[0]


def test_read_csv_projections() -> None:
    path = DATA_DIR / "projections.csv"
    df = read_projections(path)
    _check_df(df)


def test_read_json_projections() -> None:
    path = DATA_DIR / "projections.json"
    df = read_projections(path)
    _check_df(df)
