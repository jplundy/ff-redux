from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import ffa


def test_import():
    assert hasattr(ffa, "config")
