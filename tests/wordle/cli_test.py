import pytest
from click.testing import CliRunner

from wordle.cli import guess
from wordle.wordle import Wordle, WordleResults


class TestGuess:
    @pytest.fixture(autouse=True)
    def before_each(self):
        wordle = WordleResults({})
        wordle.save()

    def test_success(self):
        runner = CliRunner()
        # TODO make it more explicit. This is BAKER instead of APPLE because the index gets incremented
        # TODO incomplete, doesn't actually test success
        result = runner.invoke(guess, "BAKER")
        assert result.exit_code == 0

    def test_displays_guess_count(self):
        runner = CliRunner()
        result = runner.invoke(guess, "abcde")
        assert "1 of 6" in result.output

        result = runner.invoke(guess, "abcde")
        assert "2 of 6" in result.output

    def test_reveals_word_if_last_guess(self):
        runner = CliRunner()
        wordle = Wordle()

        for i in range(5):
            result = runner.invoke(guess, "abcde")
            assert result.exit_code == 0
            # TODO make it more explicit. This is BAKER instead of APPLE because the index gets incremented
            assert f"Todays word is: {wordle.todays_word}" not in result.output

        result = runner.invoke(guess, "abcde")
        assert result.exit_code == 0
        assert f"Today's word is: {wordle.todays_word}" in result.output

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

    def test_rejects_after_6th_guess(self):
        runner = CliRunner()

        for i in range(6):
            result = runner.invoke(guess, "abcde")
            assert result.exit_code == 0

        result = runner.invoke(guess, "abcde")
        assert result.exit_code == 2
        assert "all 6 of your guesses" in result.output
