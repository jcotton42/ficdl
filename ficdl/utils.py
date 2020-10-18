from gzip import GzipFile
from io import BytesIO
from typing import Iterable, Iterator, List
from urllib.request import urlopen

import logging
import sys

logger = logging.getLogger(__name__)

class StoryData:
    title: str
    author: str
    cover_url: str
    chapter_names: Iterable[str]
    chapter_text: Iterable[List]

    def __init__(self, title, author, cover_url, chapter_names, chapter_text):
        self.title = title
        self.author = author
        self.cover_url = cover_url
        self.chapter_names = chapter_names
        self.chapter_text = chapter_text

def download_and_decompress(url):
    with urlopen(url) as response:
        if not 200 <= response.status < 300:
            logger.critical('Failed to download story asset with HTTP status %d', response.status)
            sys.exit(2) # FIXME, should raise instead
        
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
