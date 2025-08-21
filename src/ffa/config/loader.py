from __future__ import annotations

"""Utilities for loading league configuration files."""

from pathlib import Path
from typing import Any

import yaml

from .league import LeagueConfig


def load_league_config(path: str | Path) -> LeagueConfig:
    """Load a league configuration from a YAML file.

    Parameters
    ----------
    path:
        Path to the YAML configuration file.

    Returns
    -------
    LeagueConfig
        The validated league configuration.

    Raises
    ------
    FileNotFoundError
        If the provided path does not exist.
    ValidationError
        If the YAML contents do not conform to :class:`LeagueConfig`.
    """

    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return LeagueConfig.model_validate(data)


def load_config(path: str | Path) -> dict[str, Any]:
    """Load a generic YAML configuration file into a dictionary."""

    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data or {}


def league_config_schema() -> dict[str, Any]:
    """Return the JSON schema for :class:`LeagueConfig`."""

    return LeagueConfig.model_json_schema()

