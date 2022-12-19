from dataclasses import dataclass
from functools import cached_property
import os
import yaml
from enum import Enum
from typing import TypeVar

from datetime import timezone, datetime

Self = TypeVar("Self", bound="WordleResults")


class Score(Enum):
    MISS = 0
    PARTIAL = 1
    EXACT = 2


@dataclass
class Result:
    answer: str
    guesses: list[str]


@dataclass
class LetterScore:
    letter: str
    score: Score


class WordleResults(yaml.YAMLObject):
    # TODO should this be parameterized
    results_path = os.getenv("RESULTS_PATH")
    yaml_tag = "!WordleResults"

    def __init__(self, results: dict[str, Result]):
        self.results = results

    def __repr__(self):
        return f"{self.__class__.__name__}(results={self.results})"

    @classmethod
    def load(cls) -> Self:
        with open(cls.results_path, "r") as f:
            return yaml.load(f, Loader=yaml.Loader)

    def save(self):
        with open(WordleResults.results_path, "w") as f:
            yaml.dump(self, f, Dumper=yaml.Dumper, indent=2)

    def create_result(self, date_key: str, answer: str):
        self.results.setdefault(date_key, Result(answer, []))

    def get_result(self, date_key: str) -> Result:
        return self.results.get(date_key)

    def add_guess(self, date_key, guess):
        if date_key not in self.results:
            raise IndexError(
                f"No result found for date_key: {date_key}. Call create_result first."
            )
        self.results[date_key].guesses.append(guess)


class Wordle:
    # TODO error handling or default
    MAX_GUESSES = 6

    def __init__(self):
        # TODO handle defaults/omissions/bad values
        self.results = WordleResults.load()
        # TODO hardcoded
        self.word_list_index = 1
        # TODO is this too reliant on implementation detail of create_result using setdefault
        self.results.create_result(self.todays_key, self.todays_word)

        # if len(self._results.guesses[self._today]) == 0:
        #     # TODO won't be in sync distributed
        #     # first guess, increment index
        #     self.word_list_index += 1

    @cached_property
    def word_list(self) -> list[str]:
        with open("data/answer_words.txt") as f:
            return [x.strip() for x in f]

    @property
    def todays_key(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y/%m/%d")

    @property
    def todays_word(self) -> list[str]:
        # TODO handle out of range
        return self.word_list[self.word_list_index]

    @property
    def is_last_guess(self) -> bool:
        # TODO think about whether the check below in guess is the same or just different enough to be kept separate
        return self.todays_guess_count >= Wordle.MAX_GUESSES

    @property
    def todays_guess_count(self) -> int:
        return len(self.results.get_result(self.todays_key).guesses)

    def guess(self, guess: str) -> list[LetterScore]:
        upper_guess = guess.upper()

        if self.todays_guess_count >= Wordle.MAX_GUESSES:
            raise ValueError("You've used all 6 of your guesses, try again tomorrow!")

        # e.g APPLE => {'a': 1, 'p': 2, 'l': 1, 'e': 1}
        todays_word_letter_count = {}
        for letter in list(self.todays_word):
            todays_word_letter_count[letter] = (
                todays_word_letter_count[letter] + 1
                if letter in todays_word_letter_count
                else 1
            )

        scorecard = []
        score = Score.MISS
        for i, letter in enumerate(list(upper_guess)):
            if self.todays_word[i] == letter:
                score = Score.EXACT
                todays_word_letter_count[letter] = todays_word_letter_count[letter] - 1
            elif letter in self.todays_word and todays_word_letter_count[letter] > 0:
                score = Score.PARTIAL
                todays_word_letter_count[letter] = todays_word_letter_count[letter] - 1
            else:
                score = Score.MISS
            scorecard.append(LetterScore(letter, score))

        self.results.add_guess(self.todays_key, upper_guess)
        self.results.save()
        return scorecard
