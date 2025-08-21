import subprocess


def test_cli_help_shows_commands():
    result = subprocess.run(["ffa", "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    stdout = result.stdout
    for cmd in ["init", "score", "value", "report", "backtest"]:
        assert cmd in stdout
