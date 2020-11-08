from dataclasses import dataclass
import enum
from pathlib import Path
from typing import Callable, Optional

from bs4 import PageElement

from ficdl.scrapers.types import StoryMetadata

@enum.unique
class OutputFormat(enum.Enum):
    suffix: str
    tool: Optional[str]

    EPUB = ('epub', '.epub', 'pandoc')
    PDF = ('pdf', '.pdf', 'wkhtmltopdf')

    def __new__(cls, value: str, suffix: str, tool: Optional[str]):
        obj = object.__new__(cls)
        obj._value_ = value
        obj.suffix = suffix
        obj.tool = tool

        return obj

@dataclass(eq=False, frozen=True)
class WriterOptions:
    chapter_text: list[list[PageElement]]
    metadata: StoryMetadata
    output_path: Path
    cover_path: Optional[Path]
    font_family: str
    font_size: str
    line_height: str
    page_size: str

Writer = Callable[[WriterOptions], None]
