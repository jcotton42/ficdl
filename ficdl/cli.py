from typing import Union

from pathlib import Path
import tempfile

from ficdl import __version__, __version_info__
from ficdl.utils import make_path_safe
from .callbacks import InitialStoryDetails, ChapterDetails
from .downloader import DownloadOptions, download_story, OutputFormat
from .updater import get_latest_release

def callback(details: Union[InitialStoryDetails, ChapterDetails]):
    if isinstance(details, InitialStoryDetails):
        print(f'Downloading "{details.title}" by {details.author}, with {details.chapter_count} chapters')
        print(f'Downloaded chapter 1: {details.first_chapter_title}')
    elif isinstance(details, ChapterDetails):
        print(f'Downloaded chapter {details.chatper_number}: {details.chapter_title}')
    else:
        raise Exception("jcotton42 forgot to update all the progress callbacks")

def cli_main(args):
    release = get_latest_release()
    if release.version > __version_info__:
        print("*******")
        print(f"Update available, v{'.'.join(map(str, release.version))}. (You are running {__version__})")
        print(release.download_url)
        print("*******")

    options = DownloadOptions(
        url=args.url,
        format=args.format,
        output_path=args.output,
        callback=callback,
        cover_path=args.cover,
        dump_html_to=args.dump_html_to
    )
    if args.output is not None:
        download_story(options)
    else:
        with tempfile.TemporaryDirectory() as work_dir:
            temp_path = Path(work_dir).joinpath('story.epub')
            options.output_path = temp_path
            story = download_story(options)
            dest = Path(make_path_safe(story.title) + '.' + options.format.value)
            temp_path.replace(dest)
