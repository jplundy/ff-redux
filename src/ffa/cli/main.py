from __future__ import annotations

from pathlib import Path

import typer

from ffa.reports import report as report_cmd
from ffa.scoring.core import score_projections
from ffa.sim import backtest as backtest_cmd
from ffa.value.core import calculate_values

app = typer.Typer(help="Fantasy Football Auction CLI")


@app.command()
def init(project: Path) -> None:
    """Initialize a new project at ``project``."""

    project.mkdir(parents=True, exist_ok=True)
    (project / "data").mkdir(exist_ok=True)
    (project / "output").mkdir(exist_ok=True)
    # create an empty config file
    (project / "config.yaml").touch()


@app.command()
def score(projections: Path, out: Path) -> None:
    """Score projection data and write results to ``out``."""

    score_projections(projections, out)


@app.command()
def value(scores: Path, out: Path) -> None:
    """Calculate player values from scoring results."""

    calculate_values(scores, out)

@app.command()
def report(
    config: Path = typer.Option(
        None, "--config", "-c", help="Path to configuration file"
    ),
) -> None:
    """Generate reports."""
    report_cmd(config)


@app.command()
def backtest(
    config: Path = typer.Option(
        None, "--config", "-c", help="Path to configuration file"
    ),
) -> None:
    """Run backtest simulations."""
    backtest_cmd(config)

def main() -> None:
    """Entry point used by tests and console scripts."""
    app()


if __name__ == "__main__":
    main()
