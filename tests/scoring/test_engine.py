from dataclasses import dataclass
import importlib.util
from pathlib import Path
import sys
import types
import pytest

ROOT = Path(__file__).resolve().parents[2] / "src"

# ---------------------------------------------------------------------------
# Set up minimal package structure to avoid executing full package __init__
# ---------------------------------------------------------------------------
ffa_pkg = types.ModuleType("ffa")
ffa_pkg.__path__ = [str(ROOT / "ffa")]
sys.modules.setdefault("ffa", ffa_pkg)
scoring_pkg = types.ModuleType("ffa.scoring")
scoring_pkg.__path__ = [str(ROOT / "ffa" / "scoring")]
sys.modules.setdefault("ffa.scoring", scoring_pkg)
ingest_pkg = types.ModuleType("ffa.ingest")
ingest_pkg.__path__ = [str(ROOT / "ffa" / "ingest")]
sys.modules.setdefault("ffa.ingest", ingest_pkg)

# Load schemas and engine modules directly
schemas_name = "ffa.ingest.schemas"
spec_schemas = importlib.util.spec_from_file_location(
    schemas_name, ROOT / "ffa" / "ingest" / "schemas.py"
)
schemas = importlib.util.module_from_spec(spec_schemas)
sys.modules[schemas_name] = schemas
assert spec_schemas.loader is not None
spec_schemas.loader.exec_module(schemas)
WeeklyStatRecord = schemas.WeeklyStatRecord

spec_engine = importlib.util.spec_from_file_location(
    "ffa.scoring.engine", ROOT / "ffa" / "scoring" / "engine.py"
)
engine = importlib.util.module_from_spec(spec_engine)
sys.modules["ffa.scoring.engine"] = engine
assert spec_engine.loader is not None
spec_engine.loader.exec_module(engine)
aggregate_season = engine.aggregate_season


def test_aggregate_season_sums_and_bye_weeks():
    weekly_scores = [
        WeeklyStatRecord(player_id=1, season=2023, week=1, points=10.0),
        WeeklyStatRecord(player_id=1, season=2023, week=2, points=12.0),
        WeeklyStatRecord(player_id=1, season=2023, week=4, points=5.0),  # week 3 bye
        WeeklyStatRecord(player_id=2, season=2023, week=1, points=8.0),
        WeeklyStatRecord(player_id=2, season=2023, week=2, points=8.0),
        WeeklyStatRecord(player_id=2, season=2023, week=3, points=8.0),
    ]

    totals = aggregate_season(weekly_scores)

    assert totals[1] == pytest.approx(27.0)
    assert totals[2] == pytest.approx(24.0)

    for pid, total in totals.items():
        assert total == pytest.approx(sum(aggregate_season.weekly_points[pid]))

    assert aggregate_season.weekly_points[1] == [10.0, 12.0, 0.0, 5.0]
    assert aggregate_season.weekly_points[2] == [8.0, 8.0, 8.0, 0.0]
