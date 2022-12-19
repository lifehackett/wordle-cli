import os
import yaml

import pytest
from click.testing import CliRunner

from wordle.cli import guess

SEED_DATA = {
    "word_list": ["APPLE", "BAKER", "CATCH", "BINGO"],
    "word_list_index": 0,
}


class TestGuess:
    @pytest.fixture(autouse=True)
    def before_each(self):
        try:
            datastore_path = os.getenv("DATASTORE_PATH")
            with open(datastore_path, "w") as f:
                yaml.dump(SEED_DATA, f, Dumper=yaml.Dumper, indent=2)
                pass
        except FileNotFoundError:
            pass

    def test_success(self):
        runner = CliRunner()
        # TODO make it more explicit. This is BAKER instead of APPLE because the index gets incremented
        result = runner.invoke(guess, "BAKER")
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

    def test_rejects_after_6th_guess(self):
        runner = CliRunner()

        for i in range(6):
            result = runner.invoke(guess, "abcde")
            assert result.exit_code == 0

        result = runner.invoke(guess, "abcde")
        assert result.exit_code == 2
        assert "all 6 of your guesses"
