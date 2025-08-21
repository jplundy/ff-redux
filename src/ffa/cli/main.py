from __future__ import annotations

import argparse
from pathlib import Path

from ..scoring import score_projections
from ..value import calculate_values


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="ffa")
    sub = parser.add_subparsers(dest="command", required=True)

    init_p = sub.add_parser("init", help="initialise a project directory")
    init_p.add_argument("path", type=Path)

    score_p = sub.add_parser("score", help="produce scoring from projections")
    score_p.add_argument("projections", type=Path)
    score_p.add_argument("out", type=Path)

    value_p = sub.add_parser("value", help="calculate values from scoring")
    value_p.add_argument("scoring", type=Path)
    value_p.add_argument("out", type=Path)

    args = parser.parse_args(argv)

    if args.command == "init":
        args.path.mkdir(parents=True, exist_ok=True)
        config_path = args.path / "config.yaml"
        default_cfg = {"data": "data", "output": "output"}
        import yaml

        with config_path.open("w", encoding="utf-8") as f:
            yaml.safe_dump(default_cfg, f)
        (args.path / default_cfg["data"]).mkdir(exist_ok=True)
        (args.path / default_cfg["output"]).mkdir(exist_ok=True)
        return 0

    if args.command == "score":
        score_projections(args.projections, args.out)
        return 0

    if args.command == "value":
        calculate_values(args.scoring, args.out)
        return 0

    return 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
