#!/usr/bin/env python3

import argparse
from dataclasses import dataclass
import logging
from pathlib import Path
import sys
from typing import Optional

import pypandoc

from ficdl import __version__, __version_info__
from ficdl.cli import cli_main
from ficdl.gui import gui_main
import ficdl.updater as updater
from ficdl.writers.types import OutputFormat

COULD_NOT_INSTALL_PANDOC = 1

@dataclass
class Args:
    url: Optional[str]
    output: Optional[Path]
    cover: Optional[Path]
    format: OutputFormat
    update: bool
    verbose: bool

def parse_args() -> Args:
    parser = argparse.ArgumentParser('ficdl', description='A fan fiction downloader')
    parser.add_argument('url', nargs='?', default=None, help='the URL to the story to download')
    parser.add_argument(
        '-o', '--output',
        metavar='FILE',
        type=Path,
        help='what file to output the story to. Attempts to automatically determine if not specified'
    )
    parser.add_argument(
        '-c', '--cover',
        type=Path,
        help='path to a cover for the eBook. For best results use a PNG or JPG smaller than 1,000x1,000px'
    )
    parser.add_argument(
        '-f', '--format',
        choices=[v.value for v in OutputFormat.__members__.values()],
        help='The format to save the story in. Defaults to format implied by output path, epub otherwise.'
    )

    parser.add_argument('--update', action='store_true', help='installs the latest version of ficdl')

    parser.add_argument('-v', '--verbose', action='store_true', help='output information about chapter scraping, etc.')
    parser.add_argument('-V', '--version', action='version', version='%(prog)s {}'.format(__version__))

    parsed = parser.parse_args()
    if parsed.format:
        format = OutputFormat(parsed.format)
    elif parsed.output:
        try:
            format = OutputFormat(parsed.output.suffix.lstrip('.').lower())
        except ValueError:
            parser.error(f'Unknown output format inferred from path. Please explicitly specify using `--format`.')
    else:
        format = OutputFormat.EPUB

    return Args(
        url=parsed.url,
        output=parsed.output,
        cover=parsed.cover,
        format=format,
        update=parsed.update,
        verbose=parsed.verbose,
    )

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
