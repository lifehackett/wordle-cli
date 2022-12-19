from dataclasses import dataclass
import os
import yaml
from enum import Enum
from typing import TypeVar

from datetime import timezone, datetime

Self = TypeVar("Self", bound="Wordle")


class Score(Enum):
    MISS = 0
    PARTIAL = 1
    EXACT = 2


Guesses = dict[str, list[str]]


@dataclass
class LetterScore:
    letter: str
    score: Score


class Wordle(yaml.YAMLObject):
    yaml_tag = "!Wordle"
    # TODO error handling or default
    # TODO should this be parameterized
    datastore_path = os.getenv("DATASTORE_PATH")
    MAX_GUESSES = 6

    def __init__(self, guesses: Guesses, word_list: list, word_list_index: int):
        # TODO handle defaults/omissions/bad values
        self.guesses = guesses
        self.guesses.setdefault(self._today, [])

        self.word_list = word_list
        self.word_list_index = word_list_index

        if len(self.guesses[self._today]) == 0:
            # TODO won't be in sync distributed
            # first guess, increment index
            self.word_list_index += 1

    def __repr__(self):
        return f"{self.__class__.__name__}(guesses={self.guesses}, word_list={self.word_list}, word_list_index={self.word_list_index}"

    # TODO rethink, making this private
    # @property
    # def word_list(self):
    #     return self._word_list

    @property
    def _today(self) -> str:
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
        return len(self.guesses[self._today])

    # TODO return type
    @classmethod
    def load(cls) -> Self:
        with open(cls.datastore_path, "r") as f:
            return yaml.load(f, Loader=yaml.Loader)

    def save(self):
        with open(Wordle.datastore_path, "w") as f:
            yaml.dump(self, f, Dumper=yaml.Dumper, indent=2)

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

        self.guesses[self._today].append(upper_guess)
        self.save()
        return scorecard
