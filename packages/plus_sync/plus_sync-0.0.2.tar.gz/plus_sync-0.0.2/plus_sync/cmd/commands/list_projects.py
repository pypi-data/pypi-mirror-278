from ..app import app
from ...config import Config
import typer


@app.command()
def list_remotes():
    '''
    List the available remotes.
    '''
    config = Config.from_cmdargs()
    projects = config.get_all_config_names()
    for project in projects:
        typer.echo(project)