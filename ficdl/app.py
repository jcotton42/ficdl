import logging
import sys

import pypandoc

from ficdl import __version__, __version_info__
from ficdl.cli import cli_main, parse_args
from ficdl.gui import gui_main

COULD_NOT_INSTALL_PANDOC = 1

def main():
    args = parse_args()

    try:
        pypandoc.ensure_pandoc_installed(delete_installer=True)
    except OSError:
        print('Could not find or install pandoc, install it from https://pandoc.org/ and try again.', file=sys.stderr)
        sys.exit(COULD_NOT_INSTALL_PANDOC)

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if args.url is None:
        gui_main()
    else:
        cli_main(args)
