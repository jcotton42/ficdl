from typing import Union

from .callbacks import InitialStoryDetails, ChapterDetails
from .downloader import download_story

def callback(details: Union[InitialStoryDetails, ChapterDetails]):
    if isinstance(details, InitialStoryDetails):
        print(f'Downloading "{details.title}" by {details.author}, with {details.chapter_count} chapters')
        print(f'Downloaded chapter 1: {details.first_chapter_title}')
    elif isinstance(details, ChapterDetails):
        print(f'Downloaded chapter {details.chatper_number}: {details.chapter_title}')
    else:
        raise Exception("jcotton42 forgot to update all the progress callback")

def cli_main(args):
    download_story(args.url, False, args.output, callback)
