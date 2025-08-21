"""Scoring utilities."""

from pathlib import Path

from .core import score_projections
from .engine import score_week

__all__ = ["score_week", "score_projections"]


def score(config_path: Path | None = None) -> None:
    """Placeholder for scoring logic."""
    _ = config_path

