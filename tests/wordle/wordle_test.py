import pytest

from wordle.wordle import Score, Wordle, WordleResults
from wordle.wordle_results import Result


class TestGuess:
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
        (_, scorecard) = wordle.guess("RTXXX")

        assert scorecard[0].score == Score.EXACT
        assert scorecard[1].score == Score.PARTIAL
        assert scorecard[2].score == Score.MISS
        assert scorecard[3].score == Score.MISS
        assert scorecard[4].score == Score.MISS

    @pytest.mark.freeze_time("2022-12-19")
    def test_scoring_with_duplicates(self):
        wordle = Wordle()

        # The word on 2022-12-19 is REBUT
        (_, scorecard) = wordle.guess("RTTXX")

        assert scorecard[0].score == Score.EXACT
        assert scorecard[1].score == Score.PARTIAL
        assert scorecard[2].score == Score.MISS
        assert scorecard[3].score == Score.MISS
        assert scorecard[4].score == Score.MISS


class TestMetrics:
    def test_metrics(self):
        results = WordleResults({
            "2022-12-19": Result(answer="APPLE", guesses=["APPLE"]),
            "2022-12-20": Result(answer="APPLE", guesses=["HUNCH", "REBUT", "FOCAL", "CRUST", "CRAZY", "APPLE"]),
            "2022-12-21": Result(answer="APPLE", guesses=["HUNCH", "APPLE"]),
            "2022-12-22": Result(answer="APPLE", guesses=["HUNCH", "APPLE"]),
            "2022-12-23": Result(answer="APPLE", guesses=["HUNCH", "REBUT", "FOCAL", "CRUST", "CRAZY", "CLICK"]),
            "2022-12-24": Result(answer="APPLE", guesses=["HUNCH", "REBUT"]),
        })
        wordle = Wordle(results)
        metrics = wordle.metrics()
        assert metrics.win_count == 4
        assert metrics.loss_count == 2
        assert metrics.guess_dist == [1, 2, 0, 0, 0, 1]
