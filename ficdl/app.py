#!/usr/bin/env python3

import argparse
import logging
import pypandoc
import sys

from bs4 import BeautifulSoup

from .cli import cli_main
from .downloader import download_story
from .gui import gui_main

COULD_NOT_INSTALL_PANDOC = 1

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', nargs='?', default=None, help='The URL to the story to download')
    parser.add_argument(
        '-o', '--output',
        metavar='FILE',
        help='What file to output the story to. Attempts to automatically determine if not specified.'
    )
    parser.add_argument(
        '-k', '--kindle',
        action='store_true',
        help='Produces Kindle-compatible version as well as ePub. Requires Kindle Previewer 3 to be installed.'
    )
    parser.add_argument('-v', '--verbose', action='store_true', help='Output information about chapter scraping, etc.')
    return parser.parse_args()

def main():
    try:
        pypandoc.ensure_pandoc_installed(delete_installer=True)
    except OSError:
        print('Could not find or install pandoc, install it from https://pandoc.org/ and try again.', file=sys.stderr)
        sys.exit(COULD_NOT_INSTALL_PANDOC)

    args = parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    if args.url is None:
        gui_main()
    else:
        cli_main(args)
