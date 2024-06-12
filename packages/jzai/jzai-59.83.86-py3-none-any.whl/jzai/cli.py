import click
from .bot import run_bot

@click.command()
def run():
    """Run the bot."""
    run_bot()

if __name__ == '__main__':
    run()
    