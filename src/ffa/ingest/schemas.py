"""Data ingestion contracts and schema validation utilities.

This module defines dataclass-based schemas for data ingested into the
FFA project. Each schema provides a map between field names and their
expected Polars data types along with human-readable documentation.
Helper functions validate that :class:`polars.DataFrame` instances match
these schemas before they are consumed elsewhere in the project.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, get_type_hints

import polars as pl

# ---------------------------------------------------------------------------
# Schema dataclasses
# ---------------------------------------------------------------------------


@dataclass
class PlayerRecord:
    """Basic player information.

    Attributes
    ----------
    player_id: int
        Unique identifier for the player.
    name: str
        Player's full name.
    team: str
        NFL team abbreviation (e.g. "NYG").
    position: str
        Player position code (e.g. "QB").
    """

    player_id: int
    name: str
    team: str
    position: str


@dataclass
class WeeklyStatRecord:
    """Weekly fantasy result for a player.

    Attributes
    ----------
    player_id: int
        Identifier linking the stat line to a player.
    season: int
        Four-digit season year.
    week: int
        Week number within the season starting at 1.
    points: float
        Fantasy points scored for the week.
    """

    player_id: int
    season: int
    week: int
    points: float


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

# Map basic Python types to Polars dtypes used for validation.
_PYTYPE_TO_POLARS = {
    int: pl.Int64,
    float: pl.Float64,
    str: pl.Utf8,
    bool: pl.Boolean,
}


def _dataclass_schema(dc: type) -> Dict[str, pl.DataType]:
    """Create a Polars schema dictionary from a dataclass type."""

    hints = get_type_hints(dc)
    schema: Dict[str, pl.DataType] = {}
    for name, hint in hints.items():
        try:
            schema[name] = _PYTYPE_TO_POLARS[hint]
        except KeyError as exc:  # pragma: no cover - defensive
            raise TypeError(f"Unsupported field type: {hint!r}") from exc
    return schema


# Polars schema mappings for the defined dataclasses.
PLAYER_SCHEMA = _dataclass_schema(PlayerRecord)
WEEKLY_STAT_SCHEMA = _dataclass_schema(WeeklyStatRecord)


def _format_dtype(dtype: pl.DataType) -> str:
    """Return a string representation of a Polars dtype."""
    return str(dtype)


def validate_df(df: pl.DataFrame, schema: Dict[str, pl.DataType]) -> None:
    """Validate that a DataFrame adheres to the provided schema.

    Parameters
    ----------
    df:
        The DataFrame to validate.
    schema:
        Mapping of column names to expected Polars dtypes.

    Raises
    ------
    ValueError
        If the DataFrame's columns or dtypes do not match the schema.
    """

    actual = df.schema
    missing = [c for c in schema if c not in actual]
    extra = [c for c in actual if c not in schema]
    mismatched = [
        c
        for c in schema
        if c in actual and actual[c] != schema[c]
    ]

    if missing or extra or mismatched:
        messages: Iterable[str] = []
        if missing:
            messages = [*messages, f"missing columns: {sorted(missing)}"]
        if extra:
            messages = [*messages, f"unexpected columns: {sorted(extra)}"]
        if mismatched:
            type_msgs = ", ".join(
                f"{col} expected {_format_dtype(schema[col])} got {_format_dtype(actual[col])}"
                for col in mismatched
            )
            messages = [*messages, f"dtype mismatches: {type_msgs}"]
        raise ValueError("; ".join(messages))


def validate_players(df: pl.DataFrame) -> None:
    """Validate that *df* matches :class:`PlayerRecord` schema."""

    validate_df(df, PLAYER_SCHEMA)


def validate_weekly_stats(df: pl.DataFrame) -> None:
    """Validate that *df* matches :class:`WeeklyStatRecord` schema."""

    validate_df(df, WEEKLY_STAT_SCHEMA)


__all__ = [
    "PlayerRecord",
    "WeeklyStatRecord",
    "PLAYER_SCHEMA",
    "WEEKLY_STAT_SCHEMA",
    "validate_df",
    "validate_players",
    "validate_weekly_stats",
]
