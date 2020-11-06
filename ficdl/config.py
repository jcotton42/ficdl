import dataclasses
from decimal import Decimal
import json
from pathlib import Path
import os
import os.path

from xdg import xdg_cache_home, xdg_config_home

__all__ = ['CACHE_DIR', 'CONFIG']

def _get_config_dir() -> Path:
    if os.name == 'nt':
        path = Path(os.path.expandvars('%AppData%/jcotton42/ficdl'))
    else:
        path = xdg_config_home().joinpath('jcotton42/ficdl')
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    return path

def _get_cache_dir() -> Path:
    if os.name == 'nt':
        path = Path(os.path.expandvars('%LocalAppData%/jcotton42/ficdl/cache'))
    else:
        path = xdg_cache_home().joinpath('jcotton42/ficdl')
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    return path

_CONFIG_PATH = _get_config_dir().joinpath('config.json')

@dataclasses.dataclass(eq=False)
class Config:
    default_type_face: str = 'Verdana'
    default_font_size: int = 16
    default_line_height: Decimal = Decimal('1.25')
    default_pdf_page_size: str = 'A4'

    def save(self):
        d = {}
        for f in dataclasses.fields(self):
            if f.type == Decimal:
                d[f.name] = str(getattr(self, f.name))
            else:
                d[f.name] = getattr(self, f.name)
        
        with _CONFIG_PATH.open('w', encoding='utf-8') as f:
            json.dump(d, f, indent=2, separators=(',', ': '))

def _load_config() -> Config:
    if not _CONFIG_PATH.exists():
        return Config()
    
    with _CONFIG_PATH.open('r', encoding='utf-8') as f:
        d = json.load(f)

    for field in dataclasses.fields(Config):
        if field.type == Decimal:
            d[field.name] = Decimal(d[field.name])

    return Config(**d)

CACHE_DIR = _get_cache_dir()
CONFIG = _load_config()
