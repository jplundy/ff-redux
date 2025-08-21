import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import ffa


def test_import():
    assert hasattr(ffa, "config")
