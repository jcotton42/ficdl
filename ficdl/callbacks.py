from typing import Callable, Union

class InitialStoryDetails:
    title: str
    author: str
    first_chapter_title: str
    chapter_count: int

    def __init__(self, title, author, first_chapter_title, chapter_count):
        self.title = title
        self.author = author
        self.first_chapter_title = first_chapter_title
        self.chapter_count = chapter_count

class ChapterDetails:
    chapter_title: str
    chatper_number: int
    chapter_count: int

    def __init__(self, chapter_title, chapter_number, chapter_count):
        self.chapter_title = chapter_title
        self.chatper_number = chapter_number
        self.chapter_count = chapter_count

ProgressCallback = Callable[[Union[InitialStoryDetails, ChapterDetails]], None]
