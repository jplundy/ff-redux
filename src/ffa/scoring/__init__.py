"""Scoring utilities."""

from __future__ import annotations

from pathlib import Path
import yaml

from .core import score_projections

__all__ = ["score_projections", "score"]


def score(config_path: Path | None = None) -> None:
    """Score player projections based on a simple YAML configuration.

    Parameters
    ----------
    config_path:
        Path to a YAML file containing at least a ``projections`` key pointing
        to the input CSV.  An optional ``output`` key may specify where the
        scored results should be written.  When omitted, ``scores.csv`` is
        created next to the projections file.
    """

    cfg_path = Path(config_path or "config.yaml").resolve()
    with cfg_path.open(encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}

    projections = Path(cfg["projections"]).expanduser().resolve()
    out = Path(cfg.get("output", projections.with_name("scores.csv")))

    score_projections(projections, out)

