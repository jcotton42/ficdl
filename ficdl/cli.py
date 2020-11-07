import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

from ficdl import __version__, __version_info__
from ficdl.callbacks import InitialStoryDetails, ChapterDetails
from ficdl.config import CONFIG
from ficdl.downloader import download_story, write_story
from ficdl.utils import get_font_families, make_path_safe
from ficdl.updater import get_latest_release
from ficdl.writers.types import OutputFormat, WriterOptions

@dataclass(eq=False)
class Args:
    url: Optional[str]
    output: Optional[Path]
    cover: Optional[Path]
    format: OutputFormat
    update: bool
    verbose: bool
    font_family: str
    font_size: str
    line_height: str
    page_size: str

def parse_args() -> Args:
    def path_that_exists(path: Optional[str]) -> Optional[Path]:
        if path is None:
            return None

        p = Path(path)
        if not p.exists():
            raise argparse.ArgumentTypeError(f'"{p}" does not exist')
        return p

    def font_family_that_exists(font_family: str) -> str:
        if not font_family in get_font_families(None):
            raise argparse.ArgumentTypeError(f'Font family {font_family} does not exist')
        return font_family

    parser = argparse.ArgumentParser('ficdl', description='A fan fiction downloader')
    parser.add_argument('url', nargs='?', default=None, help='the URL to the story to download')
    parser.add_argument(
        '-o', '--output',
        metavar='FILE',
        type=Path,
        help='what file to output the story to. Attempts to automatically determine if not specified',
    )
    parser.add_argument(
        '-c', '--cover',
        type=path_that_exists,
        help='path to a cover for the eBook. For best results use a PNG or JPG smaller than 1,000x1,000px',
    )
    parser.add_argument(
        '-f', '--format',
        choices=[v.value for v in OutputFormat.__members__.values()],
        help='the format to save the story in. Defaults to format implied by output path, epub otherwise',
    )
    parser.add_argument(
        '--font-family',
        type=font_family_that_exists,
        default=CONFIG.default_font_family,
        help='the font family for non-eBook formats. (default: %(default)s)',
    )
    parser.add_argument(
        '--font-size',
        default=CONFIG.default_font_size,
        help='the font size for non-eBook formats. (default: %(default)s)',
    )
    parser.add_argument(
        '--line-height',
        default=CONFIG.default_line_height,
        help='the line height for non-eBook formats. (default: %(default)s)',
    )
    parser.add_argument(
        '--page-size',
        default=CONFIG.default_page_size,
        help='the page size for non-reflowable formats (e.g. PDF). (default: %(default)s)',
    )

    parser.add_argument('--update', action='store_true', help='installs the latest version of ficdl')

    parser.add_argument('-v', '--verbose', action='store_true', help='output information about chapter scraping, etc.')
    parser.add_argument('--version', action='version', version='%(prog)s {}'.format(__version__))

    parsed = parser.parse_args()
    if parsed.format:
        format = OutputFormat(parsed.format)
    elif parsed.output:
        try:
            format = OutputFormat(parsed.output.suffix.lstrip('.').lower())
        except ValueError:
            parser.error(f'Unknown output format inferred from path. Please explicitly specify using -f or --format.')
    else:
        format = OutputFormat.EPUB

    return Args(
        url=parsed.url,
        output=parsed.output,
        cover=parsed.cover,
        format=format,
        update=parsed.update,
        verbose=parsed.verbose,
        font_family=parsed.font_family,
        font_size=parsed.font_size,
        line_height=parsed.line_height,
        page_size=parsed.page_size,
    )

def callback(details: Union[InitialStoryDetails, ChapterDetails]):
    if isinstance(details, InitialStoryDetails):
        title = details.metadata.title
        author = details.metadata.author
        chapter_count = len(details.metadata.chapter_names)
        # None means the local time zone
        date = details.metadata.update_date_utc.astimezone(None)
        print(f'Downloading "{title}" by {author}, with {chapter_count} chapters')
        print(f'Last updated {date:%Y-%m-%d}')
    elif isinstance(details, ChapterDetails):
        print(f'Downloaded chapter {details.chatper_number}: {details.chapter_title}')
    else:
        raise Exception("jcotton42 forgot to update all the progress callbacks")

def cli_main(args: Args):
    release = get_latest_release()
    if release.version > __version_info__:
        print("*******")
        print(f"Update available, v{'.'.join(map(str, release.version))}. (You are running {__version__})")
        print(release.download_url)
        print("*******")

    output = args.output
    format = args.format
    cover_path = args.cover

    metadata, text = download_story(args.url, callback)
    if output is None:
        output = Path(make_path_safe(metadata.title) + '.' + format.value)

    write_story(format, WriterOptions(
        chapter_text=text,
        metadata=metadata,
        output_path=output,
        cover_path=cover_path,
        font_family=args.font_family,
        font_size=args.font_size,
        line_height=args.line_height,
        page_size=args.page_size,
    ))
