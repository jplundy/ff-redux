from __future__ import annotations

from collections import defaultdict
from typing import Dict, Iterable, List

from ..ingest.schemas import WeeklyStatRecord


def aggregate_season(weekly_scores: Iterable[WeeklyStatRecord]) -> Dict[int, float]:
    """Aggregate weekly fantasy scores into season totals per player.

    Parameters
    ----------
    weekly_scores:
        Iterable of :class:`WeeklyStatRecord` items.

    Returns
    -------
    Dict[int, float]
        Mapping of player ID to cumulative fantasy points for the season.

    Notes
    -----
    A ``weekly_points`` attribute is attached to the function after
    execution. It maps each player ID to a list of weekly point totals.
    Missing weeks (e.g., bye weeks) are represented by ``0.0``.
    """

    totals: Dict[int, float] = defaultdict(float)
    per_player_weeks: Dict[int, Dict[int, float]] = defaultdict(dict)
    max_week = 0

    for record in weekly_scores:
        totals[record.player_id] += record.points
        per_player_weeks[record.player_id][record.week] = record.points
        if record.week > max_week:
            max_week = record.week

    weekly_points: Dict[int, List[float]] = {}
    for pid, weeks in per_player_weeks.items():
        weekly_points[pid] = [weeks.get(week, 0.0) for week in range(1, max_week + 1)]

    # Attach detailed weekly breakdown for potential future use
    aggregate_season.weekly_points = weekly_points  # type: ignore[attr-defined]

    return dict(totals)
