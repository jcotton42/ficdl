from bs4 import BeautifulSoup, Tag
from datetime import datetime
from random import uniform
from time import sleep
from typing import Optional

from .callbacks import ChapterDetails, InitialStoryDetails, ProgressCallback
from .utils import download_and_decompress, StoryData

import logging
import re

CENTER_STYLE = re.compile(r'text-align\s*:\s*center', re.IGNORECASE)

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

def extract_cover_url(page: BeautifulSoup) -> str:
    cover = page.select_one('.cimage[data-original]')
    if cover is None:
        return None
    
    url = cover['data-original']
    if url.startswith('//'):
        url = 'https:' + url
    return url

def extract_text(page: BeautifulSoup) -> list:
    text = []
    for child in page.find(id='storytext').children:
        if isinstance(child, Tag) and child.has_attr('style') and CENTER_STYLE.match(child['style']):
            # pandoc throws away the centering CSS on parsing, so add a div with a custom CSS class
            div = page.new_tag('div')
            div['class'] = 'center'
            child = child.wrap(div)
        text.append(child)

    return text

def extract_description(page: BeautifulSoup) -> str:
    return page.select_one('#profile_top > div').string

def extract_date(page: BeautifulSoup) -> datetime:
    # update date is either by itself, or the first date
    return datetime.fromtimestamp(int(page.select('#profile_top span[data-xutime]')[0]['data-xutime']))

def download_story(url: str, callback: ProgressCallback) -> StoryData:
    prefix, _chap_num, title_from_url = url.rsplit('/', maxsplit=2)

    url = f'{prefix}/1/{title_from_url}'

    first_chapter = BeautifulSoup(download_and_decompress(url), 'html5lib')
    
    title = extract_story_title(first_chapter)
    author = extract_author(first_chapter)
    cover_url = extract_cover_url(first_chapter)
    chapter_names = extract_chapter_names(first_chapter)
    chapter_text = [extract_text(first_chapter)]
    description = extract_description(first_chapter)
    date = extract_date(first_chapter)

    if chapter_names is None:
        chapter_names = [title]
    
    callback(InitialStoryDetails(title, author, chapter_names[0], len(chapter_names)))

    if len(chapter_names) > 1:
        for i in range(2, len(chapter_names) + 1):
            # rate-limiting, to be polite
            sleep(uniform(0.500, 1.250))
            url = f'{prefix}/{i}/{title_from_url}'
            chapter = BeautifulSoup(download_and_decompress(url), 'html5lib')
            chapter_text.append(extract_text(chapter))
            
            callback(ChapterDetails(chapter_names[i - 1], i, len(chapter_names)))
    
    return StoryData(title, author, cover_url, chapter_names, chapter_text, description, date)
