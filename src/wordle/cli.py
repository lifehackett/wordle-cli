from functools import reduce
import re
from datetime import timezone, datetime
from enum import Enum

import click

from wordle.local_file_storage_repository import LocalFileStorageRepository


@click.group()
def cli():
    pass


repository = LocalFileStorageRepository()


def validate_guess(ctx, param, value):
    if len(value) != 5:
        raise click.BadParameter("must be 5 characters")
    if re.match("^[a-zA-Z]{5}$", value) is None:
        raise click.BadParameter("must only contain letters")

    return value


class Score(Enum):
    MISS = 0
    PARTIAL = 1
    EXACT = 2


def add_guess(guess: str):
    # TODO handle defaults/omissions/bad values
    # TODO switch to a class based model
    word_list_index = repository.get("word_list_index")
    guesses = repository.get("guesses") or {}
    words = repository.get("word_list")
    today = datetime.now(timezone.utc).strftime("%Y/%m/%d")
    guesses.setdefault(today, [])
    if len(guesses[today]) == 0:
        # first guess, increment index
        word_list_index += 1
        repository.save("word_list_index", word_list_index)
    # TODO add back
    # if len(guesses[today]) >= 6:
    #     raise click.UsageError("You've used all 6 of your guesses, try again tomorrow!")

    # TODO handle out of range
    todays_word = list(words[word_list_index])

    todays_word_letter_count = {}
    for letter in todays_word:
        todays_word_letter_count[letter] = (
            todays_word_letter_count[letter] + 1
            if letter in todays_word_letter_count
            else 1
        )

    scorecard = []
    score = Score.MISS
    for i, letter in enumerate(list(guess)):
        if todays_word[i] == letter:
            score = Score.EXACT
            todays_word_letter_count[letter] = todays_word_letter_count[letter] - 1
        elif letter in todays_word and todays_word_letter_count[letter] > 0:
            score = Score.PARTIAL
            todays_word_letter_count[letter] = todays_word_letter_count[letter] - 1
        else:
            score = Score.MISS
        scorecard.append({"letter": letter, "score": score})

    guesses[today].append(guess)
    repository.save("guesses", guesses)

    output = []
    for result in scorecard:
        if result["score"] == Score.EXACT:
            output.append(click.style(result["letter"], bg="green"))
        elif result["score"] == Score.PARTIAL:
            output.append(click.style(result["letter"], bg="yellow"))
        else:
            output.append(result["letter"])

    click.echo("".join(output))
    # TODO if last guess output word


@click.command()
@click.argument("guess", callback=validate_guess)
def guess(guess: str):
    # TODO is this the right place for this to live?
    upper_guess = guess.upper()

    add_guess(upper_guess)
    click.echo(f"guess: {upper_guess}")


cli.add_command(guess)
