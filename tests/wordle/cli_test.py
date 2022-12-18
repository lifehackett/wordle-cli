from click.testing import CliRunner

from wordle.cli import guess


def test_guess():
    runner = CliRunner()
    result = runner.invoke(guess)
    assert result.exit_code == 0
