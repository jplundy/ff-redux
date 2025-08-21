from __future__ import annotations

import csv
from pathlib import Path


def calculate_values(scoring_file: str | Path, out_file: str | Path, multiplier: float = 1.2) -> None:
    """Calculate simple valuations from a scoring file."""
    scoring_path = Path(scoring_file)
    out_path = Path(out_file)

    with scoring_path.open(newline="", encoding="utf-8") as f_in, out_path.open(
        "w", newline="", encoding="utf-8"
    ) as f_out:
        reader = csv.DictReader(f_in)
        fieldnames = reader.fieldnames + ["Value"]
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            points = float(row["Points"])
            row["Value"] = f"{points * multiplier:.2f}"
            writer.writerow(row)
