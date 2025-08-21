from pathlib import Path

import yaml

from ffa.config import load_config


def test_load_yaml_config(tmp_path: Path) -> None:
    cfg = {"answer": 42}
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(cfg))

    loaded = load_config(path)
    assert loaded == cfg
