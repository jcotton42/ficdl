import dataclasses
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import os

if os.name == 'nt':
    from winreg import HKEY_CURRENT_USER, QueryValue

from ficdl.utils import find_tool
from ficdl.writers.epub import write_epub
from ficdl.writers.types import WriterOptions

def write_mobi(options: WriterOptions):
    try:
        kindlegen = find_tool('kindlegen')

        if kindlegen is None and os.name == 'nt':
            kindlegen = Path(
                QueryValue(HKEY_CURRENT_USER, r'Software\Amazon\Kindle Previewer 3')
            ).joinpath('lib/fc/bin/kindlegen.exe').resolve()
    except FileNotFoundError as e:
        raise Exception('Could not find KindleGen. Please install Kindle Previewer 3.') from e

    with TemporaryDirectory() as work_dir:
        work_dir = Path(work_dir)
        epub = work_dir.joinpath('temp.epub')
        write_epub(dataclasses.replace(options, output_path=str(epub)))

        # Necessary because KindleGen will only put the output mobi into
        # the same directory as the source epub. I wish I was kidding.
        temp_mobi_path = work_dir.joinpath('temp.mobi')

        subprocess.run([kindlegen, epub, '-o', str(temp_mobi_path.name)])

        temp_mobi_path.replace(options.output_path)
