import typer
from plus_sync.cmd.helpers.options import global_options
from plus_sync.config import Config
from typing import Annotated
from ..app import app

@app.command()
def init(
    project_name: Annotated[str, typer.Option(help='The name of the project.', prompt=True)],
    overwrite: Annotated[bool, typer.Option(help='Overwrite the configuration file if it already exists.')] = False
    ):
    '''
    Initialize a new configuration file.
    '''
    typer.echo(f'Initializing a new configuration file at {global_options["config_file"]}.')
    config = Config(project_name=project_name)
    try:
        config.save(global_options['config_file'], overwrite=overwrite)
    except FileExistsError as e:
        typer.echo(f'The file already exists. Use --overwrite to overwrite it.')
        raise typer.Exit(code=1)
    typer.echo('Done.')