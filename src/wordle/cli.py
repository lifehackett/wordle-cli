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
    """Guess the word of the day. All words are 5 letters long. You get 6 attempts.

    \b
    GUESS   is the word you think is the word of the day.
            must be exactly 5 letters long
    """
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

@click.command()
def metrics():
    """Print out your Wordle metrics
    """
    
    wordle = Wordle()
    metrics = wordle.metrics()
    click.echo(f"Played: {metrics.games_played}")
    click.echo(f"Win Rate: " + "{:.0%}".format(metrics.win_rate))
    click.echo(f"Guess Distribution")

    def print_guess_dist(count):
        return ''.join(['+' for i in range(count)])

    click.echo(f"1: {print_guess_dist(metrics.guess_dist[0])}")
    click.echo(f"2: {print_guess_dist(metrics.guess_dist[1])}")
    click.echo(f"3: {print_guess_dist(metrics.guess_dist[2])}")
    click.echo(f"4: {print_guess_dist(metrics.guess_dist[3])}")
    click.echo(f"5: {print_guess_dist(metrics.guess_dist[4])}")
    click.echo(f"6: {print_guess_dist(metrics.guess_dist[5])}")


cli.add_command(guess)
cli.add_command(metrics)
