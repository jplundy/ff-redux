from __future__ import annotations

import pytest

from ffa.config.league import LeagueConfig
from ffa.scoring import engine


@pytest.fixture
def league_config() -> LeagueConfig:
    """Minimal league configuration for scoring tests."""
    return LeagueConfig(
        teams=12,
        budget=200,
        roster_slots={},
        scoring_coefficients={
            "pass_yds": 0.04,
            "pass_tds": 4,
            "int": -2,
            "rush_yds": 0.1,
            "rush_tds": 6,
            "rec_yds": 0.1,
            "rec_tds": 6,
            "fum": -2,
            "two_pt": 2,
            "sack": 1,
            "dst_int": 2,
            "dst_td": 6,
            "dst_pa": -0.1,
        },
        bonuses={
            "300_pass_yds": 3,
            "100_rush_yds": 3,
            "100_rec_yds": 3,
            "shutout": 10,
        },
    )


@pytest.fixture
def weekly_stat_lines() -> list[tuple[dict[str, float], float]]:
    """Sample weekly stat lines paired with expected fantasy points."""
    return [
        (
            {
                "pass_yds": 305,
                "pass_tds": 2,
                "int": 1,
                "rush_yds": 20,
                "two_pt": 1,
            },
            25.2,
        ),
        (
            {
                "rush_yds": 110,
                "rush_tds": 1,
                "fum": 1,
            },
            18.0,
        ),
        (
            {
                "rec_yds": 150,
                "rec_tds": 1,
                "two_pt": 1,
            },
            26.0,
        ),
        (
            {
                "sack": 4,
                "dst_int": 2,
                "dst_td": 1,
                "dst_pa": 0,
            },
            24.0,
        ),
    ]


def test_weekly_parity(league_config: LeagueConfig, weekly_stat_lines: list[tuple[dict[str, float], float]]):
    """Ensure engine output matches manual weekly calculations."""
    for stats, expected in weekly_stat_lines:
        result = engine.calculate_weekly_points(stats, league_config)
        assert result == pytest.approx(expected, abs=0.1)


def test_season_aggregation(league_config: LeagueConfig):
    """Engine should aggregate weekly points across a season."""
    season_stats = [
        {"rush_yds": 50, "rush_tds": 1},
        {"rush_yds": 110, "rush_tds": 0},
        {"rush_yds": 80, "rush_tds": 1},
    ]

    manual = (
        50 * 0.1
        + 6
        + 110 * 0.1
        + 3  # 100-yard bonus
        + 80 * 0.1
        + 6
    )

    total = engine.calculate_season_points(season_stats, league_config)
    assert total == pytest.approx(manual, abs=0.1)
