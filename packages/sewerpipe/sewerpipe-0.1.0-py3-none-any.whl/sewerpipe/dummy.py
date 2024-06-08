import click
from rich.console import Console


@click.command()
@click.option("--verbose", is_flag=True, help="Will print verbose messages.")
@click.option("--name", "-n", help="Who are you?")
def main(verbose, name):
    console = Console()
    args = dict(verbose=verbose, name=name)
    console.print(f"This script has been called with the following arguments: {args}")


if __name__ == "__main__":
    main()
