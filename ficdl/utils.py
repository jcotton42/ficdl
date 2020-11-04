from gzip import GzipFile
from io import BytesIO
from urllib.request import urlopen

import logging
import re
import sys

logger = logging.getLogger(__name__)

INVALID_PATH_CHARS = re.compile(r'[<>:"/\\|?*]')
INVALID_PATH = re.compile(r'^(con|prn|aux|nul|com[1-9]|lpt[1-9])$', re.IGNORECASE)

def make_path_safe(stem: str) -> str:
    if INVALID_PATH.match(stem):
        return stem + '_'
    else:
        return INVALID_PATH_CHARS.sub('_', stem)

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
