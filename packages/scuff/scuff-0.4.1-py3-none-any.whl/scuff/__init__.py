'''
Scuff:
    A data serialization language and transpiler suite written in Python.
'''


__title__ = 'scuff'
__description__ = "A slick config file format for humans."
__url__ = "https://github.com/akyuute/scuff"
__version__ = '0.4.1'
__author__ = "akyuute"
__license__ = 'MIT'
__copyright__ = "Copyright (c) 2023-present akyuute"


ENDMARKER = ''
NEWLINE = '\n'
KEYWORDS = ()


from .tools import (
    to_json,
    to_py,
    parse,
    unparse,
    dump,
)
from .parser import (
    FileParser,
    RecursiveDescentParser,
    PyParser,
    Unparser,
)
from .compiler import Compiler

