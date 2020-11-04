import dataclasses
import logging
from pathlib import Path
from random import uniform
import tempfile
from time import sleep
from typing import Optional

from ficdl.callbacks import ChapterDetails, InitialStoryDetails, ProgressCallback
from ficdl.scrapers import get_scraper
from ficdl.scrapers.types import Scraper, StoryMetadata
from ficdl.utils import download_and_decompress
from ficdl.writers import get_writer
from ficdl.writers.types import OutputFormat, WriterOptions

logger = logging.getLogger(__name__)

@dataclasses.dataclass(eq=False)
class DownloadOptions:
    url: str
    format: OutputFormat
    output_path: Path
    callback: ProgressCallback
    cover_path: Optional[Path]

def download_story(options: DownloadOptions) -> StoryMetadata:
    url = options.url
    callback = options.callback

    scraper = get_scraper(url)
    metadata = scraper.get_metadata()
    callback(InitialStoryDetails(metadata))

    chapters = get_chapters(scraper, metadata.chapter_names, callback)

    with tempfile.TemporaryDirectory() as work_dir:
        work_dir = Path(work_dir)
        cover_path = options.cover_path
        if cover_path is None and metadata.cover_url is not None:
            cover_path = work_dir.joinpath('cover')
            with open(cover_path, 'wb') as f:
                f.write(download_and_decompress(metadata.cover_url))

        get_writer(options.format)(WriterOptions(
            chapter_text=chapters,
            metadata=metadata,
            output_path=options.output_path,
            cover_path=cover_path,
        ))

    return metadata

def get_chapters(scraper: Scraper, chatper_names: list[str], callback: ProgressCallback) -> list[list]:
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
