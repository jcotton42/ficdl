from typing import Iterable, Iterator

class StoryData:
    title: str
    author: str
    cover_url: str
    chapter_names: Iterable[str]
    chapter_text: Iterable[Iterator]

    def __init__(self, title, author, cover_url, chapter_names, chapter_text):
        self.title = title
        self.author = author
        self.cover_url = cover_url
        self.chapter_names = chapter_names
        self.chapter_text = chapter_text
