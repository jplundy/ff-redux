# Fantasy Football Auction Value Model

[![CI](https://github.com/OWNER/ff-redux/actions/workflows/ci.yml/badge.svg)](https://github.com/OWNER/ff-redux/actions/workflows/ci.yml)

This project provides a flexible framework for generating auction dollar values
for fantasy football leagues. It supports custom league configurations,
multiple data sources, and analytical techniques such as projections,
advanced stats, betting lines, and simulations.

The model uses a Value Over Replacement Player (VORP) foundation with
adjustments and calibration layers for realistic draft guidance.

## Quickstart

The repository includes toy projection and advanced statistics CSVs in the
`data/` directory. The commands below walk through initializing a league,
scoring players, valuing them for an auction draft, and producing an HTML
report.

```bash
# install the package into the current environment
pip install -e .

# create a working directory with a default league configuration
ffa init demo-league

cd demo-league

# score players using the sample projections and advanced stats
ffa score \
  --projections ../data/2024_weekly_proj \
  --advanced ../data/2024_adv_stats

# translate scores into auction dollar values
ffa value

# generate a simple HTML report
ffa report --format html --output report.html
```

The final command writes `report.html` inside `demo-league/`. Open this file in
your browser to view the results.

## Step-by-Step Guide

1. **Configure your league** – `ffa init <dir>` creates a directory containing
   `league.yaml` and placeholder data folders. Edit `league.yaml` to match your
   roster sizes, scoring settings, and auction budget.
2. **Run projections** – supply weekly projection CSVs (e.g. those under
   `data/2024_weekly_proj/`) and optional advanced stats (`data/2024_adv_stats/`).
3. **Score players** – `ffa score --projections <proj_dir> --advanced <adv_dir>`
   combines these inputs and outputs per‑player fantasy points.
4. **Calculate values** – `ffa value` converts scores into auction values based
   on your league configuration. Results are written to `values.csv`.
5. **Generate reports** – `ffa report --format html --output report.html`
   produces an HTML dashboard of the calculated values.

### Reproducing the Quickstart Example

```bash
git clone <repo-url>
cd ff-redux
pip install -e .
ffa init demo-league
cd demo-league
ffa score --projections ../data/2024_weekly_proj --advanced ../data/2024_adv_stats
ffa value
ffa report --format html --output report.html
```

Open `demo-league/report.html` after running these commands. Capture a browser
screen shot if you want to include it in your documentation.

## Project Structure

See `pyproject.toml` for tooling configuration and the `src/ffa` package for
implementation modules.
