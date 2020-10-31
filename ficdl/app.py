#!/usr/bin/env python3

import ficdl.updater as updater

import argparse
import logging
import pypandoc
import sys

from ficdl import __version__, __version_info__
from .cli import cli_main
from .gui import gui_main

COULD_NOT_INSTALL_PANDOC = 1

def parse_args():
    parser = argparse.ArgumentParser('ficdl', description='A fan fiction downloader')
    parser.add_argument('url', nargs='?', default=None, help='the URL to the story to download')
    parser.add_argument(
        '-o', '--output',
        metavar='FILE',
        help='what file to output the story to. Attempts to automatically determine if not specified'
    )
    parser.add_argument(
        '-c', '--cover',
        help='path to a cover for the eBook. For best results use a PNG or JPG smaller than 1,000x1,000px'
    )
    parser.add_argument('-v', '--verbose', action='store_true', help='output information about chapter scraping, etc.')
    parser.add_argument('-V', '--version', action='version', version='%(prog)s {}'.format(__version__))
    parser.add_argument('--update', action='store_true', help='installs the latest version of ficdl')

    parser.add_argument('--dump-html', help='debug option for dumping the generated HTML document')

    return parser.parse_args()

def main():
    args = parse_args()

    if args.update:
        release = updater.get_latest_release()
        if release.version > __version_info__:
            updater.install_update(release.download_url, False)
        else:
            print("ficdl is up to date")
            sys.exit(0)

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
