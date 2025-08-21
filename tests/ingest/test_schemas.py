"""Tests for data frame schema validation utilities."""

import polars as pl
import pytest

from ffa.ingest import schemas


def test_validate_players_passes():
    df = pl.DataFrame(
        {
            "player_id": [1],
            "name": ["Alice"],
            "team": ["NYG"],
            "position": ["QB"],
        }
    )
    schemas.validate_players(df)


def test_validate_players_missing_column():
    df = pl.DataFrame(
        {
            "player_id": [1],
            "name": ["Alice"],
            "team": ["NYG"],
        }
    )
    with pytest.raises(ValueError):
        schemas.validate_players(df)


def test_validate_players_dtype_mismatch():
    df = pl.DataFrame(
        {
            "player_id": [1],
            "name": ["Alice"],
            "team": ["NYG"],
            "position": [1],  # wrong type
        }
    )
    with pytest.raises(ValueError):
        schemas.validate_players(df)


def test_validate_weekly_stats_passes():
    df = pl.DataFrame(
        {
            "player_id": [1],
            "season": [2024],
            "week": [1],
            "points": [10.5],
        }
    )
    schemas.validate_weekly_stats(df)


def test_validate_weekly_stats_extra_column():
    df = pl.DataFrame(
        {
            "player_id": [1],
            "season": [2024],
            "week": [1],
            "points": [10.5],
            "extra": [1],
        }
    )
    with pytest.raises(ValueError):
        schemas.validate_weekly_stats(df)
