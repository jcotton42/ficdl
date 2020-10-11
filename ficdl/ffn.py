from bs4 import BeautifulSoup
from gzip import GzipFile
from io import BytesIO
from random import uniform
from time import sleep
from typing import Iterator, List, Optional
from urllib.request import urlopen

from .types import StoryData

import logging
import sys

logger = logging.getLogger(__name__)

def extract_story_title(page: BeautifulSoup) -> str:
    # sadly there is no ID for the title :/
    return page.select('#profile_top > b')[0].string

def extract_author(page: BeautifulSoup) -> str:
    # no better way for this either
    return page.select('#profile_top > a')[0].string

def extract_chapter_names(page: BeautifulSoup) -> Optional[List[str]]:
    chapters = []
    data = page.find(id='chap_select').children
    if data is None:
        # story has only 1 chapter
        return None

    for chapter in data:
        _, title = chapter.string.split('. ', maxsplit=1)
        chapters.append(title)

    return chapters

def extract_cover_url(page: BeautifulSoup) -> str:
    # stories with no cover still have the hidden big cover (it's just the generic profile image)
    # a story with an actual cover will have two elements with the cimage class
    has_cover = len(page.select('.cimage')) != 1
    if not has_cover:
        return None
    
    img = page.select('#img_large img')[0]
    url = img['src']
    if url.startswith('//'):
        url = 'https://www.fanfiction.net/' + url.lstrip('/')
    return url

def extract_text(page: BeautifulSoup) -> Iterator:
    return page.find(id='storytext').children

def download_story(url: str) -> StoryData:
    prefix, _chap_num, title_from_url = url.rsplit('/', maxsplit=2)

    url = f'{prefix}/1/{title_from_url}'

    first_chapter = BeautifulSoup(download_and_decompress(url), 'html5lib')
    
    title = extract_story_title(first_chapter)
    author = extract_author(first_chapter)
    cover_url = extract_cover_url(first_chapter)
    chapter_names = extract_chapter_names(first_chapter)
    chapter_text = [extract_text(first_chapter)]

    if chapter_names is None:
        chapter_names = [title]

    if len(chapter_names) > 1:
        for i in range(2, len(chapter_names) + 1):
            # rate-limiting, to be polite
            sleep(uniform(0.500, 1.250))
            url = f'{prefix}/{i}/{title_from_url}'
            chapter = BeautifulSoup(download_and_decompress(url), 'html5lib')
            chapter_text.append(extract_text(chapter))
    
    return StoryData(title, author, cover_url, chapter_names, chapter_text)
    
def download_and_decompress(url):
    with urlopen(url) as response:
        if not 200 <= response.status < 300:
            logger.critical('Failed to download story asset with HTTP status %d', response.status)
            sys.exit(2) # FIXME, status constant
        
        data = response.read()
        is_gzip = response.headers['Content-Encoding'] == 'gzip'
    
    return decompress(data, is_gzip)

def decompress(data, is_gzip):
    if is_gzip:
        buf = BytesIO(data)
        with GzipFile(fileobj=buf) as f:
            return f.read()
    else:
        return data
