from typing import Iterable, Tuple
from bs4 import BeautifulSoup

from bs4.element import PageElement

HTML_TEMPLATE = '''<!DOCTYPE html>
<html>
<body>
</body>
</html>'''

def make_html(chapters: Iterable[Tuple[str, list[PageElement]]]) -> BeautifulSoup:
    output = BeautifulSoup(HTML_TEMPLATE, 'html5lib')

    for (title, text) in chapters:
        h1 = output.new_tag('h1')
        h1.string = title
        output.body.append(h1)
        output.body.extend(text)

    return output
