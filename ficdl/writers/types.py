from dataclasses import dataclass
import enum
from pathlib import Path
from typing import Callable, Optional

from bs4 import PageElement

from ficdl.scrapers.types import StoryMetadata

@enum.unique
class OutputFormat(enum.Enum):
    EPUB = 'epub'
    PDF = 'pdf'

@dataclass(eq=False)
class WriterOptions:
    chapter_text: list[list[PageElement]]
    metadata: StoryMetadata
    output_path: Path
    cover_path: Optional[Path]

Writer = Callable[[WriterOptions], None]
