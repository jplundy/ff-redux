from __future__ import annotations

from pathlib import Path

import typer

from ffa.ingest import init as ingest_init
from ffa.scoring import score as scoring_score
from ffa.value import value as value_cmd
from ffa.reports import report as report_cmd
from ffa.sim import backtest as backtest_cmd

app = typer.Typer(help="Fantasy Football Auction CLI")


@app.command()
def init(
    config: Path = typer.Option(None, "--config", "-c", help="Path to configuration file"),
) -> None:
    """Initialize project resources."""
    ingest_init(config)


@app.command()
def score(
    config: Path = typer.Option(None, "--config", "-c", help="Path to configuration file"),
) -> None:
    """Run scoring logic."""
    scoring_score(config)


@app.command()
def value(
    config: Path = typer.Option(None, "--config", "-c", help="Path to configuration file"),
) -> None:
    """Calculate player values."""
    value_cmd(config)


@app.command()
def report(
    config: Path = typer.Option(None, "--config", "-c", help="Path to configuration file"),
) -> None:
    """Generate reports."""
    report_cmd(config)


@app.command()
def backtest(
    config: Path = typer.Option(None, "--config", "-c", help="Path to configuration file"),
) -> None:
    """Run backtest simulations."""
    backtest_cmd(config)


if __name__ == "__main__":
    app()


def main() -> None:
    """Entrypoint for the FFA CLI."""
    app()
