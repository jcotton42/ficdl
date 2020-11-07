import logging
from pathlib import Path
from random import uniform
import tempfile
from time import sleep
from typing import Optional, Tuple

from bs4 import PageElement

from ficdl.callbacks import ChapterDetails, InitialStoryDetails, ProgressCallback
from ficdl.config import CONFIG
from ficdl.scrapers import get_scraper
from ficdl.scrapers.types import Scraper, StoryMetadata
from ficdl.utils import download_and_decompress
from ficdl.writers import get_writer
from ficdl.writers.types import OutputFormat, WriterOptions

logger = logging.getLogger(__name__)

def download_story(url: str, callback: ProgressCallback) -> Tuple[StoryMetadata, list[list[PageElement]]]:
    scraper = get_scraper(url)
    metadata = scraper.get_metadata()
    callback(InitialStoryDetails(metadata))

    chapters = get_chapters(scraper, metadata.chapter_names, callback)

    return (metadata, chapters)

def write_story(
    metadata: StoryMetadata,
    text: list[list[PageElement]],
    format: OutputFormat,
    output_path: Path,
    cover_path: Optional[Path],
    ):
    with tempfile.TemporaryDirectory() as work_dir:
        work_dir = Path(work_dir)
        cover_path = cover_path
        if cover_path is None and metadata.cover_url is not None:
            cover_path = work_dir.joinpath('cover')
            with open(cover_path, 'wb') as f:
                f.write(download_and_decompress(metadata.cover_url))

        get_writer(format)(WriterOptions(
            chapter_text=text,
            metadata=metadata,
            output_path=output_path,
            cover_path=cover_path,
            type_face=CONFIG.default_type_face,
            font_size=CONFIG.default_font_size,
            line_height=CONFIG.default_line_height,
            page_size=CONFIG.default_pdf_page_size,
        ))

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
