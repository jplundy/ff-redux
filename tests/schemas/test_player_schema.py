import pytest

from ffa.schemas import PlayerProjection


def test_player_projection_positive_points() -> None:
    p = PlayerProjection("Jane", "RB", "FA", 10.5)
    assert p.points == 10.5


def test_player_projection_negative_points() -> None:
    with pytest.raises(ValueError):
        PlayerProjection("Jane", "RB", "FA", -1.0)
