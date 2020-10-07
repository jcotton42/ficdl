from bs4 import BeautifulSoup
from typing import Iterable, Iterator, List, Optional
from xml.sax.saxutils import escape

import logging
import os
import pypandoc
import tempfile

logger = logging.getLogger(__name__)

html_template = '''<!DOCTYPE html>
<html>
<head>
<title></title>
</head>
<body>
</body>
</html>'''

def make_output_html(story_title: str, chapters: Iterable[(str, Iterator)]) -> str:
    output = BeautifulSoup(html_template, 'html5lib')
    
    output.head.title.string = story_title

    for (title, text) in chapters:
        h1 = output.new_tag('h1')
        h1.string = title
        output.body.append(h1)
        output.body.extend(text)

    return str(output)

def create_epub(html: str, title: str, author: str, output_path: str, cover_path: Optional[str]):
    epub_metadata = f'''
    <dc:language>en-US</dc:language>
    <dc:title>{escape(title)}</dc:title>
    <dc:creator>{escape(author)}</dc:creator>
    '''

    with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
        f.write(epub_metadata)
        meta_file = f.name
    
    try:
        extra_args = [f'--epub-metadata={meta_file}']
        if cover_path:
            extra_args.append(f'--epub-cover-image={cover_path}')
        pypandoc.convert_text(
            source=html,
            format='html',
            to='epub',
            outputfile=output_path,
            extra_args=extra_args,
        )
    finally:
        try:
            os.remove(meta_file)
        except:
            logger.warn(f"Could not remove temp file '{meta_file}'")

def create_kindle(epub_path: str, output_path: str):
    # look at how pypandoc handles calling pandoc for inspiration
    ...
