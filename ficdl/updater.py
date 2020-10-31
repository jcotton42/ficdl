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
    updater = Path(tempfile.mkdtemp()).joinpath('updater.py')
    updater.write_bytes(pkgutil.get_data('ficdl', 'assets/updater.py'))

    ficdl_path = Path(ficdl.__file__).parent.parent.resolve()
    python_args = [str(updater), download_url, ficdl_path]
    if restart_app:
        python_args.append('--restart-app')

    # no that's a typo, the second sys.executable provides sys.argv[0]
    os.execl(sys.executable, sys.executable, *python_args)
