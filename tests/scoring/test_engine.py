from ffa.config import LeagueConfig
from ffa.scoring import score_week


def test_score_week_linear() -> None:
    rules = LeagueConfig(
        teams=10,
        budget=200,
        roster_slots={"QB": 1},
        scoring_coefficients={"pass_yds": 0.04, "rush_tds": 6, "turnovers": -2},
    )
    stats = {"pass_yds": 300, "rush_tds": 2, "turnovers": 1}
    expected = 300 * 0.04 + 2 * 6 + 1 * -2
    assert score_week(stats, rules) == expected


def test_score_week_bonuses() -> None:
    rules = LeagueConfig(
        teams=12,
        budget=200,
        roster_slots={"RB": 2},
        scoring_coefficients={"rush_yds": 0.1},
        bonuses={"100_rush_yds": 3, "40_long_rush_td": 1},
    )
    stats = {"rush_yds": 120, "long_rush_td": 45}
    expected = 120 * 0.1 + 3 + 1
    assert score_week(stats, rules) == expected
