from typing import Union

from ficdl import __version__, __version_info__
from .callbacks import InitialStoryDetails, ChapterDetails
from .downloader import download_story
from .updater import get_latest_version_and_uri

def callback(details: Union[InitialStoryDetails, ChapterDetails]):
    if isinstance(details, InitialStoryDetails):
        print(f'Downloading "{details.title}" by {details.author}, with {details.chapter_count} chapters')
        print(f'Downloaded chapter 1: {details.first_chapter_title}')
    elif isinstance(details, ChapterDetails):
        print(f'Downloaded chapter {details.chatper_number}: {details.chapter_title}')
    else:
        raise Exception("jcotton42 forgot to update all the progress callbacks")

def cli_main(args):
    latest_version, latest_uri = get_latest_version_and_uri()
    if latest_version > __version_info__:
        print("*******")
        print(f"Update available, v{'.'.join(map(str, latest_version))}. (You are running {__version__})")
        print(latest_uri)
        print("*******")

    download_story(args.url, False, args.output, callback)
