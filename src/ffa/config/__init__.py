"""Configuration utilities for the FFA package."""

from pathlib import Path
from typing import Any

import yaml

from .league import LeagueConfig
from .loader import league_config_schema, load_league_config


def load_config(path: str | Path) -> dict[str, Any]:
    """Load a raw YAML configuration file."""

    with Path(path).open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return data


__all__ = [
    "LeagueConfig",
    "load_league_config",
    "league_config_schema",
    "load_config",
]

