from __future__ import annotations

from dataclasses import dataclass


@dataclass
class PlayerProjection:
    """Light‑weight schema for a player's projection."""

    name: str
    position: str
    team: str
    points: float

    def __post_init__(self) -> None:
        if self.points < 0:
            raise ValueError("points must be non-negative")
