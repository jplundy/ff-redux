from ffa.ids import PlayerID


def test_player_id_from_row() -> None:
    row = {"Name": "Jane Doe", "_position": "RB", "_team": "FA"}
    pid = PlayerID.from_row(row)
    assert pid.as_tuple() == ("Jane Doe", "RB", "FA")
