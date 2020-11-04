from ficdl.writers.epub import write_epub
from ficdl.writers.types import OutputFormat, Writer

def get_writer(format: OutputFormat) -> Writer:
    if format == OutputFormat.EPUB:
        return write_epub
    else:
        raise NotImplementedError(f'Unsupported format: {format.name}')
