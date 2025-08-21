from __future__ import annotations

from pathlib import Path
import json

try:
    import yaml
except Exception:  # pragma: no cover - fallback when PyYAML missing
    yaml = None


def load_config(path: str | Path) -> dict:
    """Load a configuration file in JSON or YAML format."""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(file_path)

    if file_path.suffix in {".yaml", ".yml"}:
        if yaml is None:
            raise RuntimeError("PyYAML is required to load YAML config files")
        with file_path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    else:
        with file_path.open("r", encoding="utf-8") as f:
            return json.load(f)
