from __future__ import annotations

import csv
from pathlib import Path

from ..ids import PlayerID
from ..schemas import PlayerProjection


def score_projections(projections_file: str | Path, out_file: str | Path) -> None:
    """Read a projections CSV and extract basic scoring info."""
    projections_path = Path(projections_file)
    out_path = Path(out_file)

    players: list[PlayerProjection] = []
    with projections_path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            pid = PlayerID.from_row(row)
            points = float(row["Points"])
            players.append(
                PlayerProjection(
                    name=pid.name,
                    position=pid.position,
                    team=pid.team,
                    points=points,
                )
            )

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Name", "Position", "Team", "Points"])
        writer.writeheader()
        for p in players:
            writer.writerow(
                {
                    "Name": p.name,
                    "Position": p.position,
                    "Team": p.team,
                    "Points": p.points,
                }
            )
