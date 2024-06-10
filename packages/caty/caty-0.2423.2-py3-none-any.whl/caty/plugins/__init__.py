from .csv import CSV
from .ini import INI
from .json import JSON
from .pickle import PICKLE
from .sqlite import SQLITE
from .toml import TOML
from .txt import TXT
from .yaml import YAML
from .bin import BIN, OCT, DEC, HEX
from .cfg import CFG
from .html import HTML

Plugins = (
    CSV,
    INI,
    JSON,
    PICKLE,
    SQLITE,
    TOML,
    TXT,
    YAML,
    BIN,
    OCT,
    DEC,
    HEX,
    CFG,
    HTML,
)

config = dict(
    sort      = True,
    types     = False,
    max_seq   = 999,
    max_map   = 999,
    max_str   = 77,
    max_lines = 9,
    max_depth = 9,
    ignore    = None,
    indent    = None,
)
