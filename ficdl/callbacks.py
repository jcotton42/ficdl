from typing import Callable, Union

from ficdl.scrapers.types import StoryMetadata

class InitialStoryDetails:
    metadata: StoryMetadata

    def __init__(self, metadata: StoryMetadata):
        self.metadata = metadata

class ChapterDetails:
    chapter_title: str
    chatper_number: int
    chapter_count: int

    def __init__(self, chapter_title, chapter_number, chapter_count):
        self.chapter_title = chapter_title
        self.chatper_number = chapter_number
        self.chapter_count = chapter_count

ProgressCallback = Callable[[Union[InitialStoryDetails, ChapterDetails]], None]
