from pathlib import Path

import yaml

from ffa.config import LeagueConfig, load_league_config


def test_load_yaml_config(tmp_path: Path) -> None:
    cfg = {
        "teams": 10,
        "budget": 200,
        "roster_slots": {"QB": 1},
        "scoring_coefficients": {"pass_yds": 0.04},
    }
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(cfg))

    loaded = load_league_config(path)
    assert loaded == LeagueConfig(**cfg)
