"""Scoring utilities."""

from .core import score_projections

__all__ = ["score_projections"]


from pathlib import Path

def score(config_path: Path | None = None) -> None:
    """Placeholder for scoring logic."""
    _ = config_path

