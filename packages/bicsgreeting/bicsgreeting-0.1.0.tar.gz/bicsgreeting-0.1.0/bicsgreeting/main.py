import os
from importlib import metadata
from rich import print
import typer


app = typer.Typer()
__version__ = metadata.version(__package__)


def version_callback(value: bool) -> None:
    if value:
        print(f"[blue]{__version__}[/blue]")
        raise typer.Exit()


@app.callback()
def callback(
    _ : bool = typer.Option(None, "--version", "-v", callback=version_callback)
) -> None:
    """My app description"""


@app.command()
def hello(
    name: str = typer.Option(None, "--name", "-n", help="The person to greet.", prompt=True)
) -> None:
    """Say Hello World"""
    print(f"[green]Hello[/green] [red]{name}[/red]")


@app.command()
def getpath():
    path = os.getcwd()
    print(f"[blue]{path}[/blue]")