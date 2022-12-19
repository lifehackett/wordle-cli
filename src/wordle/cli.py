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
    YELLOW = 1
    GREEN = 2


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

    scorecard = []
    score = Score.MISS
    for i, letter in enumerate(list(guess)):
        if todays_word[i] == letter:
            score = Score.GREEN
        # TODO Multiple of same letter handling
        elif letter in todays_word:
            score = Score.YELLOW
        else:
            score = Score.MISS
        scorecard.append({"letter": letter, "score": score})

    guesses[today].append(guess)
    repository.save("guesses", guesses)

    output = []
    for score in scorecard:
        if score["score"] == Score.GREEN:
            output.append(click.style(score["letter"], bg="green"))
        elif score["score"] == Score.YELLOW:
            output.append(click.style(score["letter"], bg="yellow"))
        else:
            output.append(score["letter"])

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
