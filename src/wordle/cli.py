import click


@click.group()
def cli():
    pass


@click.command()
def guess():
    click.echo("guess")


cli.add_command(guess)
