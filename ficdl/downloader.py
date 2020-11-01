from bs4 import BeautifulSoup
from pathlib import Path
from typing import Iterable, List, Optional, Tuple
from xml.sax.saxutils import escape

import dataclasses
import enum
import logging
import pkgutil
import tempfile

import pypandoc

from ficdl.utils import download_and_decompress, StoryData
from . import ffn
from .callbacks import ProgressCallback

logger = logging.getLogger(__name__)

html_template = '''<!DOCTYPE html>
<html>
<body>
</body>
</html>'''

@enum.unique
class OutputFormat(enum.Enum):
    EPUB = 'epub'
    PDF = 'pdf'

@dataclasses.dataclass(eq=False)
class DownloadOptions:
    url: str
    format: OutputFormat
    output_path: Path
    callback: ProgressCallback
    cover_path: Optional[Path]
    dump_html_to: Optional[Path]

def download_story(options: DownloadOptions) -> StoryData:
    url = options.url
    callback = options.callback
    story = ffn.download_story(url, callback)

    html = make_output_html(zip(story.chapter_names, story.chapter_text))

    if options.dump_html_to is not None:
        with open(options.dump_html_to, 'w') as f:
            f.write(html)

    with tempfile.TemporaryDirectory() as work_dir:
        work_dir = Path(work_dir)
        cover_path = options.cover_path
        if cover_path is None and story.cover_url is not None:
            cover_path = work_dir.joinpath('cover')
            with open(cover_path, 'wb') as f:
                f.write(download_and_decompress(story.cover_url))

        if options.format == OutputFormat.EPUB:
            create_epub(html, story, options.output_path, cover_path, work_dir)
        else:
            raise NotImplementedError(f'Unimplemented output format: {options.format.name}')

    return story

def make_output_html(chapters: Iterable[Tuple[str, List]]) -> str:
    output = BeautifulSoup(html_template, 'html5lib')

    for (title, text) in chapters:
        h1 = output.new_tag('h1')
        h1.string = title
        output.body.append(h1)
        output.body.extend(text)

    return str(output)

def create_epub(html: str, metadata: StoryData, output_path: Path, cover_path: Optional[Path], work_dir: Path):
    date = metadata.date_utc.strftime('%Y-%m-%d')
    epub_metadata = f'''
    <dc:language>en-US</dc:language>
    <dc:title>{escape(metadata.title)}</dc:title>
    <dc:creator>{escape(metadata.author)}</dc:creator>
    <dc:date>{date}</dc:date>
    <dc:description>{escape(metadata.description)}</dc:description>
    '''

    meta_file = work_dir.joinpath('meta.xml')
    with open(meta_file, 'w') as f:
        f.write(epub_metadata)

    css = pkgutil.get_data('ficdl', 'assets/styles.css')
    css_file = work_dir.joinpath('styles.css')
    with open(css_file, 'wb') as f:
        f.write(css)

    extra_args = [f'--epub-metadata={meta_file}', f'--css={css_file}', '--toc']
    if cover_path:
        extra_args.append(f'--epub-cover-image={cover_path}')

    pypandoc.convert_text(
        source=html,
        format='html',
        to='epub',
        outputfile=str(output_path),
        extra_args=extra_args,
    )
