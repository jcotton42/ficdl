#!/usr/bin/env python3

from pathlib import Path

import shutil
import subprocess
import sys
import zipapp

script_dir = Path(__file__).parent
ficdl_path = script_dir.joinpath('ficdl')
dist = script_dir.joinpath('dist')

shutil.rmtree(dist, ignore_errors=True)
dist.mkdir()

shutil.copytree(ficdl_path, dist.joinpath('pkg/ficdl'))

subprocess.run([
    sys.executable,
    '-m', 'pip',
    'install',
    '--target', str(dist.joinpath('pkg')),
    '-r', str(script_dir.joinpath('requirements.txt'))
])

zipapp.create_archive(
    dist.joinpath('pkg'),
    dist.joinpath('ficdl.pyz'),
    '/usr/bin/env python3',
    'ficdl.app:main'
)
