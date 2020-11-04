from pathlib import Path
import tempfile
from typing import Union

from ficdl import __version__, __version_info__
from ficdl.callbacks import InitialStoryDetails, ChapterDetails
from ficdl.downloader import DownloadOptions, download_story
from ficdl.utils import make_path_safe
from ficdl.updater import get_latest_release

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
