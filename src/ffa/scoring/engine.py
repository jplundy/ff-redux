from __future__ import annotations

"""Core scoring engine.

This module provides functionality to compute fantasy points for a single
player's statistics in a given week according to league rules.
"""

from typing import Dict
import re

from ..config import LeagueConfig


def score_week(stats_row: Dict[str, float], rules: LeagueConfig) -> float:
    """Calculate fantasy points for a player's weekly statistics.

    Parameters
    ----------
    stats_row: dict
        Mapping of stat categories (e.g. ``pass_yds``, ``rush_tds``) to values.
    rules: LeagueConfig
        League configuration containing scoring coefficients and bonuses.

    Returns
    -------
    float
        Total fantasy points for the provided statistics.

    Notes
    -----
    The function first applies linear scoring using coefficients defined in
    ``rules.scoring_coefficients``. Bonus rules specified in ``rules.bonuses``
    are then applied. Bonus keys are expected to use a ``"<threshold>_<stat>"``
    format such as ``"100_rush_yds"`` or ``"40_long_rush_td"``. When the
    corresponding stat in ``stats_row`` meets or exceeds ``threshold`` the
    bonus is added to the final score.
    """

    score = 0.0

    # Apply linear coefficients
    for stat, coef in rules.scoring_coefficients.items():
        value = float(stats_row.get(stat, 0))
        score += value * coef

    # Apply bonuses based on thresholds
    threshold_pattern = re.compile(r"^(\d+)_([a-z_]+)$")
    for bonus_key, bonus_value in rules.bonuses.items():
        match = threshold_pattern.match(bonus_key)
        if match:
            threshold = float(match.group(1))
            stat_key = match.group(2)
            stat_value = float(stats_row.get(stat_key, 0))
            if stat_value >= threshold:
                score += bonus_value
        else:
            # Direct stat presence bonus
            stat_value = float(stats_row.get(bonus_key, 0))
            if stat_value:
                score += bonus_value

    return score
