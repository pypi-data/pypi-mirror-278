from ..app import app
from ...config import Config
import typer
from typing import Annotated


@app.command()
def list_subjects(remote_name: Annotated[str, typer.Argument(help='The name of the remote')],
                  hash_subject_ids: Annotated[bool, typer.Option(help='Whether to hash the subject IDs.')] = True):
    '''
    List the subjects in a sync endpoint.
    '''
    config = Config.from_cmdargs()
    sync = config.get_sync_by_name(remote_name)
    subjects = sync.get_all_subjects(hash=hash_subject_ids)

    typer.echo(f'Found {len(subjects)} subjects in project {remote_name}.\n')

    for subject in subjects:
        typer.echo(subject)