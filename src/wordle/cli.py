import click

from wordle.wordle import Wordle, Score


@click.group()
def cli():
    pass


def validate_guess(ctx, param, value):
    wordle = Wordle()
    try:
        wordle.validate_guess(value)
    except ValueError as e:
        raise click.BadArgumentUsage(str(e))

    return value


@click.command()
@click.argument("guess", callback=validate_guess)
def guess(guess: str):
    wordle = Wordle()

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

    click.echo(f"Guess {wordle.todays_guess_count} of {Wordle.MAX_GUESSES}")
    click.echo("".join(output))
    if not wordle.has_more_guesses and not wordle.guessed_todays_answer:
        click.echo(f"You ran out of guesses. Today's word is: {wordle.todays_answer}")


cli.add_command(guess)
