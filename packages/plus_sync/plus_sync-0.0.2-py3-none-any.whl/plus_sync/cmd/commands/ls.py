from ..app import app
from typing import Annotated
import typer
from ...config import Config


@app.command(no_args_is_help=True)
def ls(remote_name: Annotated[str, typer.Argument(help='The name of the remote to use.')],
       hash_subject_ids: Annotated[bool, typer.Option(help='Whether to hash the subject IDs.')] = True):
    '''
    List the files that are available.
    '''
    typer.echo(f'Listing the projects for {remote_name}.')
    config = Config.from_cmdargs()
    sync = config.get_sync_by_name(remote_name)
    files = sync.get_files()
    
    if hash_subject_ids:
        [x.hash_subject_ids() for x in files]
    
    for file in files:
        typer.echo(file)