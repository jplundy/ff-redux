from __future__ import annotations

import csv
from pathlib import Path

import subprocess
import sys


def run_cli(env: dict[str, str], *args: str) -> subprocess.CompletedProcess:
    cmd = [sys.executable, "-m", "ffa.cli", *args]
    return subprocess.run(cmd, check=True, capture_output=True, text=True, env=env)


def test_init_creates_config(tmp_project: Path) -> None:
    assert (tmp_project / "config.yaml").exists()
    assert (tmp_project / "data").is_dir()
    assert (tmp_project / "output").is_dir()


def test_scoring_and_valuation_pipeline(tmp_project: Path, env: dict[str, str]) -> None:
    data_file = Path("data/2024_weekly_proj/RB.csv")
    scores_out = tmp_project / "scores.csv"
    values_out = tmp_project / "values.csv"

    run_cli(env, "score", str(data_file), str(scores_out))
    assert scores_out.exists()

    run_cli(env, "value", str(scores_out), str(values_out))
    assert values_out.exists()

    with values_out.open() as f:
        reader = csv.DictReader(f)
        row = next(reader)
        assert "Value" in row and float(row["Value"]) > 0

def test_cli_help_shows_commands():
    result = subprocess.run(["ffa", "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    stdout = result.stdout
    for cmd in ["init", "score", "value", "report", "backtest"]:
        assert cmd in stdout
