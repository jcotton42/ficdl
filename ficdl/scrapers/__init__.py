from urllib.parse import urlparse

from ficdl.scrapers.ffn import FFNScraper
from ficdl.scrapers.types import Scraper

def get_scraper(url: str) -> Scraper:
    host = urlparse(url).netloc.lower()

    if host.startswith('www.'):
        host = host[4:]

    if host == 'fanfiction.net':
        return FFNScraper(url)
    else:
        raise NotImplementedError("Unsupported service")
