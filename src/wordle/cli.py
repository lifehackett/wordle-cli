import re

import click


@click.group()
def cli():
    pass


def validate_guess(ctx, param, value):
    if len(value) != 5:
        raise click.BadParameter("must be 5 characters")
    if re.match("^[a-zA-Z]{5}$", value) is None:
        raise click.BadParameter("must only contain letters")

    return value


@click.command()
@click.argument("guess", callback=validate_guess)
def guess(guess: str):

    upper_guess = guess.upper()

    click.echo(f"guess: {upper_guess}")


cli.add_command(guess)
