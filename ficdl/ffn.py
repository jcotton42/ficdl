from typing import Iterator, List

import bs4

def extract_story_title(page: bs4.BeautifulSoup) -> str:
    # sadly there is no ID for the title :/
    return page.select('#profile_top > b')[0].string

def extract_author(page: bs4.BeautifulSoup) -> str:
    # no better way for this either
    return page.select('#profile_top > a')[0].string

def extract_chapter_names(page: bs4.BeautifulSoup) -> List[str]:
    chapters = []
    for chapter in page.find(id='chap_select').children:
        _, title = chapter.string.split('. ', maxsplit=1)
        chapters.append(title)

    return chapters

def extract_text(page: bs4.BeautifulSoup) -> Iterator:
    return page.find(id='storytext').children
