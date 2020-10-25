from urllib.request import Request, urlopen

import json

class ReleaseInfo:
    def __init__(self, version, download_url, release_notes):
        self.version = version
        self.download_url = download_url
        self.release_notes = release_notes

def get_latest_release() -> ReleaseInfo:
    request = Request(
        'https://api.github.com/repos/jcotton42/ficdl/releases/latest',
        headers={'Accpet': 'application/vnd.github.v3+json'}
        )

    with urlopen(request) as respone:
        release = json.loads(respone.read())

    return ReleaseInfo(
        tuple(map(int, release['tag_name'].lstrip('v').split('.'))),
        release['html_url'],
        release['body'],
    )
