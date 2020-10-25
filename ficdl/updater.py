from urllib.request import Request, urlopen

import json

def get_latest_version_and_uri() -> tuple[tuple[int, int, int], str]:
    request = Request(
        'https://api.github.com/repos/jcotton42/ficdl/releases/latest',
        headers={'Accpet': 'application/vnd.github.v3+json'}
        )

    with urlopen(request) as respone:
        release = json.loads(respone.read())

    return (
        tuple(map(int, release['tag_name'].lstrip('v').split('.'))),
        release['html_url'],
    )
