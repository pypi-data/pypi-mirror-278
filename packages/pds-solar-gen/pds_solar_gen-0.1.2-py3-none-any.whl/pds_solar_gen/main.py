import typer
from .generator import generate
from ._version import __version__

app = typer.Typer(add_completion=False)
app.command(
    name="generate",
    help="Use your data file to generate ProteusDS files.",
)(generate)


@app.command()
def info():
    """Show version info"""
    typer.echo(f"Using pds-solar-gen v{__version__}")


app(prog_name="pds-solar-gen")
