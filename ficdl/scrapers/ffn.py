from bs4 import BeautifulSoup, PageElement, Tag
from datetime import datetime, timezone
from typing import Optional

from ficdl.scrapers.types import Scraper, StoryMetadata
from ficdl.utils import download_and_decompress

import logging
import re

CENTER_STYLE = re.compile(r'text-align\s*:\s*center', re.IGNORECASE)
UNDERLINE_STYLE = re.compile(r'text-decoration\s*:\s*underline', re.IGNORECASE)

logger = logging.getLogger(__name__)

def extract_story_title(page: BeautifulSoup) -> str:
    # sadly there is no ID for the title :/
    return page.select('#profile_top > b')[0].string

def extract_author(page: BeautifulSoup) -> str:
    # no better way for this either
    return page.select('#profile_top > a')[0].string

def extract_chapter_names(page: BeautifulSoup) -> Optional[list[str]]:
    chapters = []
    data = page.find(id='chap_select')
    if data is None:
        # story has only 1 chapter
        return None

    for chapter in data.children:
        _, title = chapter.string.split('. ', maxsplit=1)
        chapters.append(title)

    return chapters

def extract_cover_url(page: BeautifulSoup) -> Optional[str]:
    cover = page.select_one('.cimage[data-original]')
    if cover is None:
        return None
    
    url = cover['data-original']
    if url.startswith('//'):
        url = 'https:' + url
    return url

def extract_text(page: BeautifulSoup) -> list[PageElement]:
    text = []
    for child in page.find(id='storytext').children:
        if isinstance(child, Tag) and child.name == 'p':
            if child.has_attr('style') and CENTER_STYLE.match(child['style']):
                # pandoc throws away the centering CSS on parsing, so add a div with a custom CSS class
                div = page.new_tag('div')
                div['class'] = 'center'
                del child['style']
                child = child.wrap(div)
            for span in child.find_all(name='span', style=UNDERLINE_STYLE):
                span['class'] = 'underline'
                del span['style']

        text.append(child)

    return text

def extract_description(page: BeautifulSoup) -> str:
    return page.select_one('#profile_top > div').string

def extract_update_date_utc(page: BeautifulSoup) -> datetime:
    # update date is either by itself, or the first date
    return datetime.fromtimestamp(int(page.select('#profile_top span[data-xutime]')[0]['data-xutime']), timezone.utc)

DEFAULT_HEADERS = {
    'Referer': 'https://www.fanfiction.net/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36 Edg/87.0.664.47',
}

class FFNScraper(Scraper):
    base_url: str
    title_from_url: str
    first_chapter: BeautifulSoup

    def __init__(self, url: str) -> None:
        self.base_url, _chap_num, self.title_from_url = url.rsplit('/', maxsplit=2)

    def get_metadata(self) -> StoryMetadata:
        url = f'{self.base_url}/1/{self.title_from_url}'

        if getattr(self, 'first_chapter', None) is None:
            page, _mimetype = download_and_decompress(url, headers=DEFAULT_HEADERS)
            self.first_chapter = BeautifulSoup(page, 'html5lib')

        title = extract_story_title(self.first_chapter)
        author = extract_story_title(self.first_chapter)
        cover_url = extract_cover_url(self.first_chapter)
        chapter_names = extract_chapter_names(self.first_chapter)
        description = extract_description(self.first_chapter)
        update_date_utc = extract_update_date_utc(self.first_chapter)

        if chapter_names is None:
            chapter_names = [title]

        return StoryMetadata(
            title=title,
            author=author,
            cover_url=cover_url,
            chapter_names=chapter_names,
            description=description,
            update_date_utc=update_date_utc
        )

    def get_text_for_chapter(self, number: int) -> list[PageElement]:
        if number == 1 and self.first_chapter is not None:
            chapter = self.first_chapter
        else:
            url = f'{self.base_url}/{number}/{self.title_from_url}'
            page, _mimetype = download_and_decompress(url, headers=DEFAULT_HEADERS)
            chapter = BeautifulSoup(page, 'html5lib')

        return extract_text(chapter)
