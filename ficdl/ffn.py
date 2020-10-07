from typing import Iterator

import bs4

def extract_story_title(page: bs4.BeautifulSoup) -> str:
    # sadly there is no ID for the title :/
    return page.select('#profile_top > b')[0].string

def extract_author(page: bs4.BeautifulSoup) -> str:
    # no better way for this either
    return page.select('#profile_top > a')[0].string

def extract_chapters(page: bs4.BeautifulSoup) -> dict:
    chapters = {}
    for chapter in page.find(id='chap_select').children:
        num, title = chapter.string.split('. ', maxsplit=1)
        chapters[num] = title

    return chapters

def extract_text(page: bs4.BeautifulSoup) -> Iterator:
    return page.find(id='storytext').children
