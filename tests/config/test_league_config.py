from pathlib import Path
import sys

import pytest
from pydantic import ValidationError

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from ffa.config import LeagueConfig, league_config_schema, load_league_config


def test_load_league_config_valid():
    config_path = Path(__file__).resolve().parents[2] / "src/ffa/config/template/league.yaml"
    config = load_league_config(config_path)
    assert isinstance(config, LeagueConfig)
    assert config.teams == 12
    assert config.roster_slots["QB"] == 1


def test_load_league_config_invalid(tmp_path):
    bad_file = tmp_path / "bad.yaml"
    bad_file.write_text("teams: 12\n")  # missing required fields
    with pytest.raises(ValidationError):
        load_league_config(bad_file)


def test_league_config_schema():
    schema = league_config_schema()
    assert schema["title"] == "LeagueConfig"
    for field in ["teams", "budget", "roster_slots", "scoring_coefficients"]:
        assert field in schema["properties"]
