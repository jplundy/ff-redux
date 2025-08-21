"""Scoring utilities."""

from .core import score_projections
from .engine import aggregate_season

__all__ = ["score_projections", "aggregate_season"]


from pathlib import Path

def score(config_path: Path | None = None) -> None:
    """Placeholder for scoring logic."""
    _ = config_path

