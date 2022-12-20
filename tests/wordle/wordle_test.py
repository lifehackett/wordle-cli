import pytest

from wordle.wordle import Score, Wordle, WordleResults


class TestGuess:
    @pytest.fixture(autouse=True)
    def before_each(self):
        wordle = WordleResults({})
        wordle.save()

    def test_too_short_failure(self):
        wordle = Wordle()

        with pytest.raises(ValueError):
            wordle.guess("abcd")

    def test_too_long_failure(self):
        wordle = Wordle()

        with pytest.raises(ValueError):
            wordle.guess("abcdef")

    def test_too_many_guesses(self):
        wordle = Wordle()

        for i in range(6):
            wordle.guess("abcde")

        with pytest.raises(ValueError):
            wordle.guess("abcdef")

    @pytest.mark.freeze_time("2022-12-19")
    def test_scoring(self):
        wordle = Wordle()

        # The word on 2022-12-19 is REBUT
        scorecard = wordle.guess("RTXXX")

        assert scorecard[0].score == Score.EXACT
        assert scorecard[1].score == Score.PARTIAL
        assert scorecard[2].score == Score.MISS
        assert scorecard[3].score == Score.MISS
        assert scorecard[4].score == Score.MISS

    @pytest.mark.freeze_time("2022-12-19")
    def test_scoring_with_duplicates(self):
        wordle = Wordle()

        # The word on 2022-12-19 is REBUT
        scorecard = wordle.guess("RTTXX")

        assert scorecard[0].score == Score.EXACT
        assert scorecard[1].score == Score.PARTIAL
        assert scorecard[2].score == Score.MISS
        assert scorecard[3].score == Score.MISS
        assert scorecard[4].score == Score.MISS
