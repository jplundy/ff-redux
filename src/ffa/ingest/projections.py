"""Utilities for reading player projection data."""

from __future__ import annotations

from pathlib import Path
import json

import polars as pl

from ffa.ids import PlayerID


def _normalize_columns(df: pl.DataFrame) -> pl.DataFrame:
    """Rename common projection columns to our canonical names."""

    rename_map = {
        "Player": "name",
        "Name": "name",
        "Team": "team",
        "_team": "team",
        "Position": "position",
        "_position": "position",
        "Week": "week",
        "Points": "points",
    }
    df = df.rename({k: v for k, v in rename_map.items() if k in df.columns})
    return df


def _attach_player_ids(df: pl.DataFrame) -> pl.DataFrame:
    """Add a ``player_id`` column derived from ``PlayerID``."""

    players = (
        df.select(["name", "position", "team"])
        .unique()
        .sort(["name", "position", "team"])
    )

    mapping: dict[tuple[str, str, str], int] = {}
    for idx, row in enumerate(players.iter_rows(named=True), start=1):
        pid = PlayerID(row["name"], row["position"], row["team"])
        mapping[pid.as_tuple()] = idx

    ids = [
        mapping[(row["name"], row["position"], row["team"])]
        for row in df.iter_rows(named=True)
    ]

    return df.with_columns(pl.Series("player_id", ids, dtype=pl.Int64))


def _fill_missing_weeks(df: pl.DataFrame) -> pl.DataFrame:
    """Insert zero-point rows for weeks with no projections."""

    max_week = int(df["week"].max())
    players = df.select(["player_id", "name", "team", "position"]).unique()
    weeks = pl.DataFrame({"week": list(range(1, max_week + 1))})
    full = players.join(weeks, how="cross")
    df = full.join(df, on=["player_id", "week"], how="left")
    df = df.with_columns(pl.col("points").fill_null(0.0))
    df = df.select(["player_id", "name", "team", "position", "week", "points"])
    return df.sort(["player_id", "week"])


def _process(df: pl.DataFrame) -> pl.DataFrame:
    df = _normalize_columns(df)
    df = df.select(["name", "team", "position", "week", "points"])
    df = df.with_columns(
        [
            pl.col("name").cast(pl.Utf8),
            pl.col("team").cast(pl.Utf8),
            pl.col("position").cast(pl.Utf8),
            pl.col("week").cast(pl.Int64),
            pl.col("points").cast(pl.Float64),
        ]
    )
    df = _attach_player_ids(df)
    df = _fill_missing_weeks(df)
    return df


def read_csv_projections(path: str | Path) -> pl.DataFrame:
    """Read projection data from a CSV file."""

    df = pl.read_csv(path)
    return _process(df)


def read_json_projections(path: str | Path) -> pl.DataFrame:
    """Read projection data from a JSON file."""

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    df = pl.DataFrame(data)
    return _process(df)


def read_projections(path: str | Path) -> pl.DataFrame:
    """Read projections from either CSV or JSON based on file extension."""

    ext = Path(path).suffix.lower()
    if ext == ".csv":
        return read_csv_projections(path)
    if ext == ".json":
        return read_json_projections(path)
    raise ValueError(f"Unsupported projection source: {path}")


__all__ = [
    "read_csv_projections",
    "read_json_projections",
    "read_projections",
]
