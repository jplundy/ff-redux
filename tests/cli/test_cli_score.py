from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import csv


def run_cli(env: dict[str, str], *args: str) -> subprocess.CompletedProcess:
    cmd = [sys.executable, "-m", "ffa.cli", *args]
    return subprocess.run(cmd, check=True, capture_output=True, text=True, env=env)


def test_score_command_produces_output(tmp_path: Path, env: dict[str, str]) -> None:
    """Running ``ffa score`` should generate a scored CSV file."""

    projections = Path("data/2024_weekly_proj/RB.csv")
    out_file = tmp_path / "scores.csv"

    config = tmp_path / "score.yaml"
    config.write_text(
        f"projections: {projections}\noutput: {out_file}\n", encoding="utf-8"
    )

    run_cli(env, "score", "--config", str(config))

    assert out_file.exists()
    with out_file.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        row = next(reader)
        assert {"Name", "Position", "Team", "Points"} <= row.keys()


def test_cli_help_lists_score_command(env: dict[str, str]) -> None:
    result = subprocess.run(
        [sys.executable, "-m", "ffa.cli", "--help"], capture_output=True, text=True, env=env
    )
    assert result.returncode == 0
    assert "score" in result.stdout

