from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass(eq=False)
class StoryMetadata:
    title: str
    author: str
    cover_url: Optional[str]
    chapter_names: list[str]
    description: str
    update_date_utc: datetime

class Scraper(metaclass=ABCMeta):
    @abstractmethod
    def get_metadata(self) -> StoryMetadata:
        pass

    @abstractmethod
    def get_text_for_chapter(self, number: int) -> list:
        pass
