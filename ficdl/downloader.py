from ficdl.utils import download_and_decompress, StoryData
from bs4 import BeautifulSoup
from typing import Iterable, List, Optional, Tuple
from xml.sax.saxutils import escape

import logging
import os
import os.path
import pypandoc
import re
import tempfile

from . import ffn
from .callbacks import ProgressCallback

logger = logging.getLogger(__name__)

html_template = '''<!DOCTYPE html>
<html>
<body>
</body>
</html>'''

invalid_path_chars = re.compile(r'[<>:"/\\|?*]')
invalid_names = [
    'con',
    'prn',
    'aux',
    'nul',
    'com1',
    'com2',
    'com3',
    'com4',
    'com5',
    'com6',
    'com7',
    'com8',
    'com9',
    'lpt1',
    'lpt2',
    'lpt3',
    'lpt4',
    'lpt5',
    'lpt6',
    'lpt7',
    'lpt8',
    'lpt9'
]

def download_story(url: str, cover_path: Optional[str], output_path: str, callback: ProgressCallback):
    story = ffn.download_story(url, callback)

    html = make_output_html(zip(story.chapter_names, story.chapter_text))

    with tempfile.TemporaryDirectory() as work_dir:
        if cover_path is None and story.cover_url is not None:
            cover_path = os.path.join(work_dir, 'cover')
            with open(cover_path, 'wb') as f:
                f.write(download_and_decompress(story.cover_url))

        create_epub(html, story, output_path, cover_path, work_dir)

def make_output_html(chapters: Iterable[Tuple[str, List]]) -> str:
    output = BeautifulSoup(html_template, 'html5lib')

    for (title, text) in chapters:
        h1 = output.new_tag('h1')
        h1.string = title
        output.body.append(h1)
        output.body.extend(text)

    return str(output)

def create_epub(html: str, metadata: StoryData, output_path: str, cover_path: Optional[str], work_dir: str):
    date = metadata.date_utc.strftime('%Y-%m-%d')
    epub_metadata = f'''
    <dc:language>en-US</dc:language>
    <dc:title>{escape(metadata.title)}</dc:title>
    <dc:creator>{escape(metadata.author)}</dc:creator>
    <dc:date>{date}</dc:date>
    <dc:description>{escape(metadata.description)}</dc:description>
    '''

    meta_file = os.path.join(work_dir, 'meta.xml')
    with open(meta_file, 'w') as f:
        f.write(epub_metadata)

    extra_args = [f'--epub-metadata={meta_file}', '--toc']
    if cover_path:
        extra_args.append(f'--epub-cover-image={cover_path}')
    pypandoc.convert_text(
        source=html,
        format='html',
        to='epub',
        outputfile=output_path,
        extra_args=extra_args,
    )

def create_kindle(epub_path: str, output_path: str):
    # look at how pypandoc handles calling pandoc for inspiration
    ...
