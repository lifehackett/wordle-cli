import re

import click

from wordle.wordle import Wordle, Score


@click.group()
def cli():
    pass


# TODO move validation logic to Wordle...maybe
def validate_guess(ctx, param, value):
    if len(value) != 5:
        raise click.BadParameter("must be 5 characters")
    if re.match("^[a-zA-Z]{5}$", value) is None:
        raise click.BadParameter("must only contain letters")

    return value


@click.command()
@click.argument("guess", callback=validate_guess)
def guess(guess: str):
    wordle = Wordle.load()

    scorecard = []
    try:
        scorecard = wordle.guess(guess)
    except ValueError as e:
        raise click.UsageError(e)

    output = []
    for result in scorecard:
        if result.score == Score.EXACT:
            output.append(click.style(result.letter, bg="green"))
        elif result.score == Score.PARTIAL:
            output.append(click.style(result.letter, bg="yellow"))
        else:
            output.append(result.letter)

    click.echo("".join(output))
    if wordle.is_last_guess:
        click.echo(f"Today's word is: {wordle.todays_word}")


cli.add_command(guess)
