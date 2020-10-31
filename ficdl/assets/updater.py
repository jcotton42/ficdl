#!/usr/bin/env python3

from pathlib import Path

import argparse
import shutil
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument('source_path')
parser.add_argument('install_path')
parser.add_argument('work_dir')
parser.add_argument('--restart-app', action='store_true')
args = parser.parse_args()

source_path = Path(args.source_path)
install_path = Path(args.install_path)
work_dir = args.work_dir
restart_app = args.restart_app

mode = install_path.stat().st_mode
source_path.replace(install_path)
install_path.chmod(mode)

if restart_app:
    subprocess.Popen([sys.executable, install_path])

shutil.rmtree(work_dir, ignore_errors=True)
