from pathlib import Path
from typing import NoReturn
from urllib.request import Request, urlopen

import json
import os
import pkgutil
import tempfile
import sys

import ficdl

class ReleaseInfo:
    def __init__(self, version, download_url, release_notes):
        self.version = version
        self.download_url = download_url
        self.release_notes = release_notes

def get_latest_release() -> ReleaseInfo:
    request = Request(
        'https://api.github.com/repos/jcotton42/ficdl/releases/latest',
        headers={'Accpet': 'application/vnd.github.v3+json'}
        )

    with urlopen(request) as respone:
        release = json.loads(respone.read())

    return ReleaseInfo(
        tuple(map(int, release['tag_name'].lstrip('v').split('.'))),
        release['assets'][0]['url'],
        release['body'],
    )

def install_update(download_url: str, restart_app: bool) -> NoReturn:
    work_dir = Path(tempfile.mkdtemp())

    updater = work_dir.joinpath('updater.py')
    updater.write_bytes(pkgutil.get_data('ficdl', 'assets/updater.py'))

    current_ficdl_path = Path(ficdl.__file__).parent.parent.resolve()
    updated_ficdl_path = work_dir.joinpath('ficdl.pyz')

    request = Request(download_url, headers={
        'accept': 'application/octet-stream',
    })

    with urlopen(request) as response:
        updated_ficdl_path.write_bytes(response.read())

    python_args = [
        str(updater),
        str(updated_ficdl_path),
        str(current_ficdl_path),
        str(work_dir)
    ]
    if restart_app:
        python_args.append('--restart-app')

    # no that's a typo, the second sys.executable provides sys.argv[0]
    os.execl(sys.executable, sys.executable, *python_args)
