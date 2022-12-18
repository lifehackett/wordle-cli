from click.testing import CliRunner

from wordle.cli import guess


# def test_guess():
#     runner = CliRunner()
#     result = runner.invoke(guess)
#     assert result.exit_code == 0


class TestGuess:
    def test_success(self):
        runner = CliRunner()
        result = runner.invoke(guess, "abcde")
        assert result.exit_code == 0

    def test_rejects_empty_input(self):
        runner = CliRunner()
        result = runner.invoke(guess)
        assert result.exit_code == 2
        assert "Missing argument" in result.output

    def test_rejects_less_than_5_char_guess(self):
        runner = CliRunner()
        result = runner.invoke(guess, "four")
        assert result.exit_code == 2
        assert "must be 5 characters" in result.output

    def test_rejects_more_than_5_char_guess(self):
        runner = CliRunner()
        result = runner.invoke(guess, "morethanfive")
        assert result.exit_code == 2
        assert "must be 5 characters" in result.output

    def test_rejects_non_alpha_characters(self):
        runner = CliRunner()
        result = runner.invoke(guess, "abcd1")
        assert result.exit_code == 2
        assert "must only contain letters" in result.output
