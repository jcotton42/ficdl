from pathlib import Path
import pkgutil
import shutil
from string import Template
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

        with css_path.open('w', encoding='utf-8') as f:
            f.write(pkgutil.get_data('ficdl', 'assets/styles.css').decode('utf-8'))
            f.write('\n')
            pdf_css = Template(
                pkgutil.get_data('ficdl', 'assets/pdf.css').decode('utf-8')
            ).substitute(
                font_family=options.font_family,
                font_size=options.font_size,
                line_height=options.line_height,
            )
            f.write(pdf_css)

        html_path.write_text(str(html), encoding='utf-8')

        args = [
            'wkhtmltopdf',
            '--title', metadata.title,
            '--print-media-type',
            '--footer-center', '[page]',
            '--allow', str(work_dir),
            '--page-size', options.page_size,
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
