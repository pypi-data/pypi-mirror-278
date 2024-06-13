from pathlib import Path
import typer
import yaml
from rich.console import Console

import pds_solar_gen.file_defs as f


app = typer.Typer()
console = Console()


@app.command()
def generate(
    nrows: int = typer.Argument(
        3,
        help="Number of platform rows",
    ),
    ncols: int = typer.Argument(
        3,
        help="Number of platform columns",
    ),
    config_file: Path = typer.Argument(
        Path("config.yaml"),
        readable=True,
        exists=True,
        help="The path to the directory where the config file exists",
    ),
    outdir: Path = typer.Argument(
        Path("pds_sim"),
        writable=True,
        file_okay=False,
        dir_okay=True,
        help="The path to the directory where the simulation files should be written."
        " Default: 'pds_sim'.",
    ),
):
    """CLI command function that takes the number of rows and columns
    and drops them in the output directory.
    """

    with open(config_file, "r") as file:
        cfg = yaml.safe_load(file)

    # Thruster properties
    thruster = cfg["thrusters"]
    # Solar panel properties
    solar_panel = cfg["solar_panel"]
    # Float properties
    floats = cfg["floats"]
    # Connections
    connections = cfg["connections"]
    # Array heading (convert to deg from N)
    heading = cfg["array"]["platform_heading"] - 180
    # Array float spacing from (0,0), center of main float
    spacing = cfg["array"]["float_spacing"]
    # Float connection points
    joints = cfg["array"]["float_joints"]

    if floats["perimeter"]:
        ncols += 2

    filepath = str(outdir)
    f.check_configurations(thruster, floats)
    f.create_directory(filepath)
    f.create_sim(filepath, nrows, ncols)
    f.create_env(filepath)
    f.create_ini(filepath, nrows, ncols, floats, solar_panel)
    f.create_dat(filepath, nrows, ncols, spacing, heading)
    f.create_lib(filepath, nrows, ncols, floats, solar_panel, connections, joints)
    f.create_thrusters(filepath, thruster)

    return


if __name__ == "__main__":
    app()
    # app(generate(2, 5, Path("config.yaml"), Path("pds_sim")))
