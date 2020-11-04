from pathlib import Path
from typing import Union

from ficdl import __version__, __version_info__
from ficdl.callbacks import InitialStoryDetails, ChapterDetails
from ficdl.downloader import download_story, write_story
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

    output = args.output
    format = args.format
    cover_path = args.cover

    metadata, text = download_story(args.url, callback)
    if output is None:
        output = Path(make_path_safe(metadata.title) + '.' + format.value)

    write_story(metadata, text, format, output, cover_path)
