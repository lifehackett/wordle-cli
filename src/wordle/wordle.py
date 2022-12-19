from dataclasses import dataclass
from functools import cached_property
from enum import Enum
import re

from datetime import timezone, datetime, date

from wordle.wordle_results import WordleResults


class Score(Enum):
    MISS = 0
    PARTIAL = 1
    EXACT = 2


@dataclass
class LetterScore:
    letter: str
    score: Score


class Wordle:
    MAX_GUESSES = 6

    def __init__(self):
        self.results = WordleResults.load()
        day_zero = date(2022, 12, 18)
        today = date.today()
        self.answer_list_index = (today - day_zero).days
        if not self.results.get_result(self.todays_key):
            self.results.create_result(self.todays_key, self.todays_answer)

    @cached_property
    def answer_list(self) -> list[str]:
        """Get list of possible answers

        Returns:
            list[str]: the words
        """
        with open("data/answer_words.txt") as f:
            return [x.strip() for x in f]

    @property
    def todays_key(self) -> str:
        """Get today's date formatted correctly for use as a key in results entries

        Returns:
            str: the key
        """
        return datetime.now(timezone.utc).strftime("%Y/%m/%d")

    @property
    def todays_answer(self) -> list[str]:
        """Get today's answer

        Raises:
            Exception: Ran out of words. This can happen if you play the game for a while. Will release a patch before that happens ;)

        Returns:
            list[str]: today's answer
        """
        try:
            return self.answer_list[self.answer_list_index]
        except IndexError:
            raise Exception("Ran out of words!")

    @property
    def has_more_guesses(self) -> bool:
        """Do you have more guesses for today

        Returns:
            bool:
        """
        return self.todays_guess_count < Wordle.MAX_GUESSES

    @property
    def todays_guesses(self) -> list[str]:
        """Get todays guesses

        Returns:
            list[str]: today's guesses
        """
        return self.results.get_result(self.todays_key).guesses

    @property
    def todays_guess_count(self) -> int:
        """Get the number of guesses already made today

        Returns:
            int:
        """
        return len(self.todays_guesses)

    @property
    def guessed_todays_answer(self) -> bool:
        """Has today's word already been guessed

        Returns:
            bool:
        """
        return self.todays_answer in self.todays_guesses

    def validate_guess(self, guess: str):
        """Validate the guess attempt meets the critera

        A guess must be exactly 5 letters, casing doesn't matter.

        Args:
            guess (str): the guess

        Raises:
            ValueError: if the guess is too short or too long
            ValueError: if the guess has non a-Z A-Z characters (letters)
            ValueError: if they have already reached their guess limit
            ValueError: if they have already guessed today's word
        """
        if len(guess) != 5:
            raise ValueError("must be 5 characters")
        if re.match("^[a-zA-Z]{5}$", guess) is None:
            raise ValueError("must only contain letters")
        if self.todays_guess_count >= Wordle.MAX_GUESSES:
            raise ValueError("You've used all 6 of your guesses, try again tomorrow!")
        if self.guessed_todays_answer:
            raise ValueError(f"You already guessed today's word! {self.todays_answer}")

    def guess(self, guess: str) -> list[LetterScore]:
        """Takes a guess and checks to see whether it matches the answer

        The guess will be tokenized and each letter will receive a score of:
        EXACT - the letter is both correct and in the correct position
        PARTIAL - the letter exists in the word, but is in the wrong location. Duplicates will only be flagged if the answer also conatins duplications
        MISS - the letter is not in the word

        Args:
            guess (str): the guess

        Returns:
            list[LetterScore]: The guess, tokenized by letter with each letter assigned a score
        """
        self.validate_guess(guess)

        upper_guess = guess.upper()

        # e.g APPLE => {'a': 1, 'p': 2, 'l': 1, 'e': 1}
        todays_answer_letter_count = {}
        for letter in list(self.todays_answer):
            todays_answer_letter_count[letter] = (
                todays_answer_letter_count[letter] + 1
                if letter in todays_answer_letter_count
                else 1
            )

        scorecard = []
        score = Score.MISS
        for i, letter in enumerate(list(upper_guess)):
            if self.todays_answer[i] == letter:
                score = Score.EXACT
                todays_answer_letter_count[letter] = (
                    todays_answer_letter_count[letter] - 1
                )
            elif (
                letter in self.todays_answer and todays_answer_letter_count[letter] > 0
            ):
                score = Score.PARTIAL
                todays_answer_letter_count[letter] = (
                    todays_answer_letter_count[letter] - 1
                )
            else:
                score = Score.MISS
            scorecard.append(LetterScore(letter, score))

        self.results.add_guess(self.todays_key, upper_guess)
        self.results.save()
        return scorecard
