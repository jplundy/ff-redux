"""Subpackage for ingest functionality."""

from pathlib import Path
import shutil


_TEMPLATE = Path(__file__).resolve().parents[1] / "config" / "template" / "league.yaml"


def init(config_path: Path | None = None) -> None:
    """Set up a project directory with a default configuration.

    Parameters
    ----------
    config_path:
        Location where the league configuration should be written.  If *None*,
        ``config.yaml`` in the current directory is used.  The parent directory
        along with ``data`` and ``output`` folders are created if they do not
        already exist.
    """

    cfg = Path(config_path or "config.yaml").resolve()
    project_dir = cfg.parent
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / "data").mkdir(exist_ok=True)
    (project_dir / "output").mkdir(exist_ok=True)

    if not cfg.exists():
        shutil.copyfile(_TEMPLATE, cfg)
