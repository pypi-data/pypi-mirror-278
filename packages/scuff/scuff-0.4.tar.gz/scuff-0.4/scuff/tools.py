__all__ = (
    'to_json',
    'to_py',
    'parse',
    'unparse',
    'dump',
)


import ast
import json
import os
from ast import AST, Module
from os import PathLike

from .compiler import Compiler
from .lexer import Lexer
from .parser import RecursiveDescentParser, FileParser, PyParser, Unparser


type JSONData = str
type PythonData = str
type ScuffText = str


def parse(source: PathLike | ScuffText) -> Module:
    '''
    Parse Scuff text or a file containing it and return its AST.

    :param source: Scuff to parse or the path to a file containing it.
    :type source: :class:`ScuffText` | :class:`PathLike`
    '''
    if os.path.exists(source):
        absolute = os.path.abspath(os.path.expanduser(source))
        node = FileParser(absolute).parse()
    elif isinstance(source, ScuffText.__value__):
        node = RecursiveDescentParser(string=source).parse()
    else:
        raise ValueError(
            f"`source` must be valid Scuff or a file path as a string,"
            f" not type {type(source)!r}."
        )
    return node


def dump(
    source: AST | PathLike | ScuffText,
    annotate_fields: bool = True,
    include_attributes: bool = False,
    *,
    indent: int | str | None = 2
) -> str:
    '''
    Return a formatted dump of the abstract syntax tree given by `source`
    or gotten by parsing it.
    If `source` is not an AST, use the `parse` function to obtain one.
    This is mainly useful for debugging purposes.
    All other parameters are fed directly into :func:`ast.parse`.

    :param source: The AST, Scuff to parse or the path to a file
        containing it.
    :type source: :class:`AST` | :class:`PathLike` | :class:`ScuffText`

    :param annotate_fields: Display unambiguous field names,
        defaults to ``True``
    :type annotate_fields: :class:`bool`

    :param include_attributes: Display additional attributes such as line
        numbers and column offsets, defaults to ``False``
    :type include_attributes: :class:`bool`

    :param indent: Pretty-print the tree with this indent level.
        If ``None``, display as a single line, defaults to ``2``
    :type indent: :class:`int` | :class:`str` | ``None``
    '''
    if isinstance(source, AST):
        node = source
    elif os.path.exists(source):
        absolute = os.path.abspath(os.path.expanduser(source))
        node = FileParser(absolute).parse()
    elif isinstance(source, ScuffText.__value__):
        node = RecursiveDescentParser(string=source).parse()
    else:
        raise ValueError(
            f"`source` must be valid Scuff or a file path as a string,"
            f" not type {type(source)!r}."
        )
    return ast.dump(node, annotate_fields, include_attributes, indent=indent)


def unparse(node: AST) -> ScuffText:
    '''
    Convert an AST back into Scuff text.

    :param node: The AST to unparse
    :type node: :class:`AST`
    '''
    return Unparser().unparse(node)


def py_to_scuff(data: PythonData) -> ScuffText:
    '''
    Convert Python data to Scuff.

    :param data: The Python object to convert
    :type data: :class:`PythonData`
    '''
    return PyParser.to_scuff(data)


def to_py(source: PathLike | ScuffText) -> PythonData:
    '''
    Convert Scuff to Python data.

    :param source: Scuff to parse or the path to a file containing it.
    :type source: :class:`ScuffText` | :class:`PathLike`
    '''
    node = parse(source)
    data = Compiler().compile(node)
    return data


def to_json(source: PathLike | ScuffText) -> JSONData:
    '''
    Convert Scuff to JSON.

    :param source: Scuff to parse or the path to a file containing it.
    :type source: :class:`ScuffText` | :class:`PathLike`
    '''
    data = to_py(source)
    return json.dumps(data)

