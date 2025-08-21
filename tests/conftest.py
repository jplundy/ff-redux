from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

# Ensure local ``src`` is on the import path for tests
SRC = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC))


@pytest.fixture
def env() -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(SRC)
    return env


@pytest.fixture
def tmp_project(tmp_path: Path, env: dict[str, str]) -> Path:
    """Create a temporary FFA project directory using ``ffa init``."""
    proj = tmp_path / "project"
    subprocess.run([sys.executable, "-m", "ffa.cli", "init", str(proj)], check=True, env=env)
    return proj
