#!/usr/bin/env python3

from pathlib import Path
from urllib.request import Request, urlopen

import argparse
import shutil
import subprocess
import sys
import tempfile

parser = argparse.ArgumentParser()
parser.add_argument('download_url')
parser.add_argument('install_path')
parser.add_argument('--restart-app', action='store_true')
args = parser.parse_args()

download_url = args.download_url
install_path = Path(args.install_path)
restart_app = args.restart_app

work_path = Path(__file__).resolve().parent
download_path = work_path.joinpath('ficdl.pyz')

request = Request(download_url, headers={
    'accept': 'application/octet-stream'
})

with urlopen(request) as response:
    with download_path.open('wb') as f:
        f.write(response.read())

download_path.replace(install_path)

mode = install_path.stat().st_mode
# makes file executable for those that can read it
# https://stackoverflow.com/a/30463972
mode |= (mode & 0o444) >> 2
install_path.chmod(mode)

if restart_app:
    subprocess.Popen([sys.executable, install_path])

if Path(tempfile.gettempdir()) in work_path.parents:
    shutil.rmtree(work_path, ignore_errors=True)
