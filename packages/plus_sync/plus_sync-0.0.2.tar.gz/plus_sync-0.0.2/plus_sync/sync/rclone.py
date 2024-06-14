import json
from .base import BaseSync, FileInformation
import plus_sync.config
import subprocess
from fnmatch import fnmatch


class RCloneAccess(BaseSync):
    def __init__(self, config: 'plus_sync.config.RCloneConfig'):
        self.config = config

    def _get_files(self, with_metadata=True):
        all_files = []
        for cur_path in self.config.remote_paths:
            this_files_json = self._rclone('lsjson', '-R', '--hash', self._remote_path(cur_path))
            this_files = json.loads(this_files_json)
            this_files = [x for x in this_files if not x['IsDir']]
            this_files = [x for x in this_files if any(fnmatch(x['Path'], glob) for glob in self.config.globs)]
            this_files = [FileInformation(path=f'{cur_path}/{x["Path"]}', size=x['Size'], last_modified=x['ModTime'], hashes=x['Hashes']) for x in this_files]
            all_files.extend(this_files)

        return all_files

    def get_content(self, file: FileInformation) -> bytes:
        return subprocess.run(['rclone', 'cat', self._remote_path(file.path)], capture_output=True).stdout
    
    def _rclone(self, cmd: str, *args) -> str:
        return subprocess.run(['rclone', cmd, *args], capture_output=True).stdout.decode()
    
    def _remote_path(self, path: str) -> str:
        return f'{self.config.remote}:{self.config.remote_base_folder}/{path}'