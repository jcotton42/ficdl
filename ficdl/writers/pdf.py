from pathlib import Path
import pkgutil
import shutil
import subprocess
from tempfile import TemporaryDirectory

from ficdl.writers.common import make_html
from ficdl.writers.types import WriterOptions

def write_pdf(options: WriterOptions):
    text = options.chapter_text
    metadata = options.metadata
    output_path = options.output_path
    cover_path = options.cover_path

    html = make_html(zip(metadata.chapter_names, text))

    with TemporaryDirectory() as work_dir:
        work_dir = Path(work_dir)
        css_path = work_dir.joinpath('styles.css')
        html_path = work_dir.joinpath('story.html')

        css_path.write_bytes(pkgutil.get_data('ficdl', 'assets/styles.css'))
        html_path.write_text(str(html), encoding='utf-8')

        args = [
            'wkhtmltopdf',
            '--title', metadata.title,
            '--print-media-type',
            '--footer-center', '[page]',
            '--allow', Path(work_dir),
        ]

        if cover_path is not None:
            cover_html_path = work_dir.joinpath('cover.html')
            cover_html_path.write_bytes(pkgutil.get_data('ficdl', 'assets/pdf-cover.html'))

            shutil.copyfile(cover_path, work_dir.joinpath('cover'))

            args.extend([
                'cover', str(cover_html_path), '--encoding', 'utf-8',
            ])
        else:
            # no cover image
            ...

        args.extend([
            'toc', '--toc-header-text', 'Chapters',
            str(html_path), '--encoding', 'utf-8', '--user-style-sheet', str(css_path),
            str(output_path),
        ])

        subprocess.run(args)
