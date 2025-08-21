from __future__ import annotations

"""Pydantic model for league configuration."""

from typing import Dict

from pydantic import BaseModel, Field


class LeagueConfig(BaseModel):
    """Configuration model for a fantasy football league.

    Attributes
    ----------
    teams: int
        Number of teams participating in the league.
    budget: int
        Budget available to each team for drafting players.
    roster_slots: Dict[str, int]
        Mapping of roster positions to the number of slots for each.
    scoring_coefficients: Dict[str, float]
        Coefficients applied to various statistics for scoring.
    bonuses: Dict[str, float]
        Optional bonuses awarded for achieving certain milestones.
    thresholds: Dict[str, float]
        Thresholds used for categorizing player performance.
    """

    teams: int
    budget: int
    roster_slots: Dict[str, int]
    scoring_coefficients: Dict[str, float]
    bonuses: Dict[str, float] = Field(default_factory=dict)
    thresholds: Dict[str, float] = Field(default_factory=dict)
