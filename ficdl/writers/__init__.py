from ficdl.writers.epub import write_epub
from ficdl.writers.mobi import write_mobi
from ficdl.writers.pdf import write_pdf
from ficdl.writers.types import OutputFormat, Writer

def get_writer(format: OutputFormat) -> Writer:
    if format == OutputFormat.EPUB:
        return write_epub
    elif format == OutputFormat.MOBI:
        return write_mobi
    elif format == OutputFormat.PDF:
        return write_pdf
    else:
        raise NotImplementedError(f'Unsupported format: {format.name}')
