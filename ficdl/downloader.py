import dataclasses
import logging
import mimetypes
from pathlib import Path
from random import uniform
import tempfile
from time import sleep
from typing import Tuple

from bs4 import PageElement

from ficdl.callbacks import ChapterDetails, InitialStoryDetails, ProgressCallback
from ficdl.scrapers import get_scraper
from ficdl.scrapers.types import Scraper, StoryMetadata
from ficdl.utils import download_and_decompress
from ficdl.writers import get_writer
from ficdl.writers.types import OutputFormat, WriterOptions

logger = logging.getLogger(__name__)

# horrible hack, the C# version will be better I promise
DEFAULT_HEADERS = {
    'Referer': 'https://www.fanfiction.net/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47',
}

def download_story(url: str, callback: ProgressCallback) -> Tuple[StoryMetadata, list[list[PageElement]]]:
    scraper = get_scraper(url)
    metadata = scraper.get_metadata()
    callback(InitialStoryDetails(metadata))

    chapters = get_chapters(scraper, metadata.chapter_names, callback)

    return (metadata, chapters)

def write_story(format: OutputFormat, writer_options: WriterOptions):
    with tempfile.TemporaryDirectory() as work_dir:
        work_dir = Path(work_dir)
        cover_path = writer_options.cover_path
        if cover_path is None and writer_options.metadata.cover_url is not None:
            image, mime = download_and_decompress(writer_options.metadata.cover_url, headers=DEFAULT_HEADERS)

            if len(image) > 0:
                # handles the image CDN going down, story text often still works though
                # should emit a warning here
                suffix = mimetypes.guess_extension(mime)
                cover_path = work_dir.joinpath('cover').with_suffix(suffix)
                with open(cover_path, 'wb') as f:
                    f.write(image)
            else:
                cover_path = None

            writer_options = dataclasses.replace(writer_options, cover_path=cover_path)

        get_writer(format)(writer_options)

def get_chapters(scraper: Scraper, chatper_names: list[str], callback: ProgressCallback) -> list[list[PageElement]]:
    text = []
    for ch in range(1, len(chatper_names) + 1):
        # a random delay to be polite
        sleep(uniform(0.500, 1.250))
        callback(ChapterDetails(
            chapter_title=chatper_names[ch - 1],
            chapter_number=ch,
            chapter_count=len(chatper_names),
        ))

        text.append(scraper.get_text_for_chapter(ch))

    return text
