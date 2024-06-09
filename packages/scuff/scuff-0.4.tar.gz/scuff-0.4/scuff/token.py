import string
from enum import Enum
from os import PathLike
from typing import Any

from . import ENDMARKER, NEWLINE


type Lexer = 'Lexer'
type LineNo = int
type CharNo = int
type ColNo = int
type TokenValue = str
type Location = tuple[LineNo, ColNo]


ENDMARKER = ''
NEWLINE = '\n'
KEYWORDS = ()


class TokType(Enum):
    NEWLINE = repr(NEWLINE)
    ENDMARKER = repr(ENDMARKER)
    COMMENT = 'COMMENT'
    SPACE = 'SPACE'
    NAME = 'NAME'
    FLOAT = 'FLOAT'
    INTEGER = 'INTEGER'
    STRING = 'STRING'
    TRUE = 'TRUE'
    FALSE = 'FALSE'
    NONE = 'NONE'

    LPAR = '('
    RPAR = ')'
    LSQB = '['
    RSQB = ']'
    COLON = ':'
    COMMA = ','
    SEMI = ';'
    PLUS = '+'
    MINUS = '-'
    STAR = '*'
    SLASH = '/'
    DOUBLESLASH = '//'
    VBAR = '|'
    AMPER = '&'
    LESS = '<'
    GREATER = '>'
    EQUAL = '='
    DOT = '.'
    PERCENT = '%'
    LBRACE = '{'
    RBRACE = '}'
    EQEQUAL = '=='
    NOTEQUAL = '!='
    LESSEQUAL = '<='
    GREATEREQUAL = '>='
    TILDE = '~'
    CIRCUMFLEX = '^'
    LEFTSHIFT = '<<'
    RIGHTSHIFT = '>>'
    DOUBLESTAR = '**'
    EXCLAMATION = '!'
    QUESTION = '?'
    UNKNOWN = 'UNKNOWN'

    def __or__(self, other: Any) -> str:
        return type(self).__name__ + ' | ' + type(other).__name__


class TokGroup:
    '''
    '''
    T_Literal = {
        TokType.STRING,
        TokType.INTEGER,
        TokType.FLOAT,
        TokType.TRUE,
        TokType.FALSE,
        TokType.NONE,
    }
    T_AssignEvalNone = {TokType.NEWLINE, TokType.ENDMARKER}
    T_Ignore = {TokType.SPACE, TokType.COMMENT}
    T_Invisible = {*T_Ignore, TokType.NEWLINE}
    T_Syntax = {
        TokType.LSQB,
        TokType.LBRACE,
        TokType.LPAR,
        TokType.RSQB,
        TokType.RBRACE,
        TokType.RPAR,
    }


class Token:
    '''
    Represents a single lexical word in a config file.

    :param at: The token's location
    :type at: tuple[:class:`CharNo`, :class:`Location`]

    :param value: The literal text making up the token
    :type value: :class:`str`

    :param type: The token's distict type
    :type type: :class:`TokType`

    :param matchgroups: The value gotten by re.Match.groups() when
        making this token
    :type matchgroups: tuple[:class:`str`]

    :param lexer: The lexer used to find this token, optional
    :type lexer: :class:`Lexer`

    :param file: The file from which this token came, optional
    :type file: :class:`PathLike`
    '''
    __slots__ = (
        'at',
        'value',
        'type',
        'matchgroups',
        'cursor',
        'lineno',
        'colno',
        'lexer',
        'file',
    )

    def __init__(
        self,
        at: tuple[CharNo, Location],
        value: TokenValue,
        type: TokType,
        matchgroups: tuple[str],
        lexer: Lexer = None,
        file: PathLike = None,
    ) -> None:
        self.at = at
        self.value = value
        self.type = type
        self.matchgroups = matchgroups
        self.cursor = at[0]
        self.lineno = at[1][0]
        self.colno = at[1][1]
        self.lexer = lexer
        self.file = file

    def __repr__(self):
        cls = type(self).__name__
        ignore = ('matchgroups', 'cursor', 'lineno', 'colno', 'lexer', 'file')
        pairs = (
            (k, getattr(self, k)) for k in self.__slots__
            if k not in ignore
        )
        stringified = tuple(
            # Never use repr() for `Enum` instances:
            (k, repr(v) if isinstance(v, str) else str(v))
            for k, v in pairs
        )
        
        attrs = ', '.join(('='.join(pair) for pair in stringified))
        s = f"{cls}({attrs})"
        return s

    def __lt__(self, other) -> bool:
        return self.cursor < other.cursor

    def __le__(self, other) -> bool:
        return self.cursor <= other.cursor

    def __gt__(self, other) -> bool:
        return self.cursor > other.cursor

    def __ge__(self, other) -> bool:
        return self.cursor >= other.cursor

    def __class_getitem__(cls, item: TokType) -> str:
        return cls
        item_name = (
            item.__class__.__name__
            if not hasattr(item, '__name__')
            else item.__name__
        )
        return f"{cls.__name__}[{item_name}]"

    def error_leader(self, with_col: bool = False) -> str:
        '''
        Return the beginning of an error message that features the
        filename, line number and possibly current column number.

        :param with_col: Also print the current column number,
            defaults to ``False``
        :type with_col: :class:`bool`
        '''
        file = f"File {self.file}, " if self.file is not None else ''
        column = ', column ' + str(self.colno) if with_col else ''
        msg = f"{file}Line {self.lineno}{column}: "
        return msg

    @property
    def match_repr(self) -> str | None:
        '''
        Return the token's value in quotes, if parsed as a string,
        else ``None``
        '''
        if not len(self.matchgroups) > 1:
            return None
        quote = self.matchgroups[0]
        val = self.value
        return f"{quote}{val}{quote}"

    @property
    def coords(self) -> Location:
        '''
        Return the token's current coordinates as (line, column).
        '''
        return (self.lineno, self.colno)
    

