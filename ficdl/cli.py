from typing import Union

import os
import os.path
import tempfile

from ficdl import __version__, __version_info__
from ficdl.utils import make_path_safe
from .callbacks import InitialStoryDetails, ChapterDetails
from .downloader import download_story
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

    if args.output is not None:
        download_story(args.url, args.cover, args.output, args.dump_html, callback)
    else:
        with tempfile.TemporaryDirectory() as work_dir:
            temp_path = os.path.join(work_dir, 'story.epub')
            story = download_story(args.url, args.cover, temp_path, args.dump_html, callback)
            name = make_path_safe(story.title)
            os.replace(temp_path, name + ".epub")
