from pathlib import Path
import pkgutil
from string import Template
from tempfile import TemporaryDirectory
from xml.sax.saxutils import escape

import pypandoc

from ficdl.writers.common import make_html
from ficdl.writers.types import WriterOptions

EPUB_METADATA_TEMPLATE = Template('''
<dc:language>$language</dc:language>
<dc:title>$title</dc:title>
<dc:creator>$author</dc:creator>
<dc:date>$date</dc:date>
<dc:description>$description</dc:description>
''')

def write_epub(options: WriterOptions):
    metadata = options.metadata
    output_path = options.output_path
    cover_path = options.cover_path

    epub_metadata = EPUB_METADATA_TEMPLATE.substitute(
        language='en-US',
        title=escape(metadata.title),
        author=escape(metadata.author),
        date=metadata.update_date_utc.strftime('%Y-%m-%d'),
        description=escape(metadata.description),
    )

    html = make_html(zip(metadata.chapter_names, options.chapter_text))

    with TemporaryDirectory() as work_dir:
        work_dir = Path(work_dir)
        meta_file = work_dir.joinpath('meta.xml')
        css_file = work_dir.joinpath('styles.css')

        meta_file.write_text(epub_metadata, encoding='utf-8')
        css_file.write_bytes(pkgutil.get_data('ficdl', 'assets/styles.css'))

        extra_args = [
            f'--epub-metadata={str(meta_file)}',
            f'--css={str(css_file)}',
            '--toc',
        ]
        if cover_path:
            extra_args.append(f'--epub-cover-image={str(cover_path)}')

        pypandoc.convert_text(
            source=str(html),
            format='html',
            to='epub',
            outputfile=str(output_path),
            extra_args=extra_args,
        )
