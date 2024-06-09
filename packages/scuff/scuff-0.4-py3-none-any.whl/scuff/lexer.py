import re
import string
from enum import Enum
from os import PathLike
from typing import Any, Self

from . import ENDMARKER, KEYWORDS, NEWLINE
from .error import TokenError
from .token import (
    Token,
    TokGroup,
    CharNo,
    ColNo,
    LineNo,
    Location,
    TokType,
)


NOT_IN_IDS = string.punctuation.replace('_', r'\s')


class Lexer:
    '''
    The lexer splits text apart into individual tokens.

    :param string: If not using a file, use this string for lexing.
    :type string: :class:`str`

    :param file: The file to use for lexing.
        When unset or ``None``, use `string` by default.
    :type file: :class: `PathLike`
    '''
    STRING_CONCAT = False  # Concatenate neighboring strings
    SPEECH_CHARS = tuple('"\'`') + ('"""', "'''", "```")
    MULTILINE_QUOTES = SPEECH_CHARS[-3:]

    _rules = (
        # Data types

        ## Multiline strings
        (re.compile(
            r'^(?P<speech_char>["\'`]{3})'
            r'(?P<text>((?!(?P=speech_char)).|' + NEWLINE + r')*)'
            r'(?P=speech_char)'
        , re.MULTILINE), TokType.STRING),

        ## Single-line strings
        (re.compile(
            r'^(?P<speech_char>["\'`])'
            r'(?P<text>((?!(?P=speech_char)).)*)'
            r'(?P=speech_char)'
        ), TokType.STRING),

        ## Numbers
        (re.compile(
            r'^\d?(\d*|[\d_]*\d)'
            r'\.'
            # Match trailing '_' and catch resulting Py ValueError later:
            r'\d[\d_]*'
        ), TokType.FLOAT),
            # Again here:
        (re.compile(r'^\d[\d_]*'), TokType.INTEGER),

        ## None/null
        (re.compile(r'^(none|null)', re.IGNORECASE), TokType.NONE),

        ## Booleans
        (re.compile(r'^(true|yes)', re.IGNORECASE), TokType.TRUE),
        (re.compile(r'^(false|no)', re.IGNORECASE), TokType.FALSE),

        # Ignore
        ## Comments
        (re.compile(r'^\#.*(?=\n*)'), TokType.COMMENT),
        ## Matching Newline helps find empty assignments:
        (re.compile(r'^' + NEWLINE + r'+'), TokType.NEWLINE),
        ## All other whitespace
        (re.compile(r'^[^' + NEWLINE + r'\S]+'), TokType.SPACE),

        # Operators
        (re.compile(r'^\='), TokType.EQUAL),
        (re.compile(r'^\.'), TokType.DOT),
        (re.compile(r'^\-'), TokType.MINUS),
        (re.compile(r'^\+'), TokType.PLUS),
        (re.compile(r'^\!'), TokType.EXCLAMATION),
        (re.compile(r'^\~'), TokType.TILDE),

        # Syntax
        (re.compile(r'^\,'), TokType.COMMA),
        (re.compile(r'^\('), TokType.LPAR),
        (re.compile(r'^\)'), TokType.RPAR),
        (re.compile(r'^\['), TokType.LSQB),
        (re.compile(r'^\]'), TokType.RSQB),
        (re.compile(r'^\{'), TokType.LBRACE),
        (re.compile(r'^\}'), TokType.RBRACE),

        # Symbols
        *((r'^' + kw, TokType.KEYWORD) for kw in KEYWORDS),
        (re.compile(r'^[^' + NOT_IN_IDS + r']+'), TokType.NAME),
    )

    __slots__ = (
        '_string',
        '_lines',
        '_tokens',
        '_token_stack',
        '_string_debug',
        'eof',
        '_cursor',
        '_lineno',
        '_colno',
        '_file',
    )

    def __init__(
        self,
        string: str = None,
        file: str = None
    ) -> None: 
        self._string = string
        self._lines = self._string.split('\n')
        self._tokens = []
        self._token_stack = []
        self._string_debug = None
        self.eof = ENDMARKER

        self._cursor = 0  # 0-indexed
        self._lineno = 1  # 1-indexed
        self._colno = 1  # 1-indexed
        self._file = file

    @property
    def lineno(self) -> int:
        '''
        Return the current line number.
        '''
        return self._string[:self._cursor].count('\n') + 1

    def curr_line(self) -> str:
        '''
        Return the text of the current line.
        '''
        return self._lines[self._lineno - 1]

    def get_line(self, lookup: LineNo | Token) -> str:
        '''
        Retrieve a line using its line number or a token.

        :param lookup: Use this line number or token to get the line.
        :type lookup: :class:`LineNo` | :class:`Token`
        :returns: The text of the line gotten using `lookup`
        :rtype: :class:`str`
        '''
        if isinstance(lookup, Token):
            lineno = lookup.at[1][0]
        else:
            lineno = lookup
        return self._lines[lineno - 1]

    @property
    def coords(self) -> Location:
        '''
        Return the lexer's current coordinates as (line, column).
        '''
        return (self._lineno, self._colno)
    
    def lex(self, string: str = None) -> list[Token]:
        '''
        Return a list of tokens from lexing.
        Optionally lex a new string `string`.

        :param string: The string to lex, if not `self._string`
        :type string: :class:`str`
        '''
        if string is not None:
            self._string = string

        tokens = []
        try:
            while True:
                tok = self.get_token()
                tokens.append(tok)
                if tok.type is TokType.ENDMARKER:
                   break
        except TokenError as e:
            import traceback
            traceback.print_exc(limit=1)
            raise 

        self.reset()
        return tokens

    def reset(self) -> Self:
        '''
        Move the lexer back to the beginning of the string.
        '''
        self._cursor = 0
        self._lineno = 1
        self._colno = 1
        self._tokens = []
        return self

    def in_range(self, first: Token, last: Token) -> tuple[Token]:
        '''
        Gather tokens from between a range spanned by two tokens.

        :param first: The first token to gather
        :type first: :class:`Token`

        :param last: The last token to gather
        :type last: :class:`Token`
        '''
        tokens = self._tokens
        if last not in tokens and last.type not in TokGroup.T_Invisible:
            tokens.append(last)
        start = first.cursor
        end = last.cursor
        between = tuple(t for t in tokens if start <= t.cursor <= end)
        return between

    def get_prev(self, back: int = 1, since: Token = None) -> tuple[Token]:
        '''
        Retrieve tokens from before the current position of the lexer.

        :param back: How many tokens before the current token to look,
            defaults to 1
        :type back: :class:`int`

        :param since: Return every token after this token.
        :type since: :class:`Token`
        '''
        if since is None:
            return tuple(self._tokens[-back:])
        tokens = self._tokens
        idx = tuple(tok.cursor for tok in tokens).index(since.cursor)
        ret = tuple(tokens[idx - back : idx + 1])
        return ret

    def error_leader(self, with_col: bool = False) -> str:
        '''
        Return the beginning of an error message that features the
        filename, line number and possibly current column number.

        :param with_col: Also print the current column number,
            defaults to ``False``
        :type with_col: :class:`bool`
        '''
        # file = self._file if self._file is not None else ''
        column = ', column ' + str(self._colno) if with_col else ''
        # msg = f"File {file!r}, line {self._lineno}{column}: "
        msg = f"Line {self._lineno}{column}: "
        return msg

    def get_token(self) -> Token:
        '''
        Return the next token in the lexing stream.

        :raises: :exc:`TokenError` upon an unexpected token
        '''
        try:
            return next(self._get_token())
        except StopIteration as e:
            return e.value

    def _get_token(self) -> Token:
        '''
        A generator.
        Return the next token in the lexing stream.

        :raises: :exc:`StopIteration` to give the current token
        :raises: :exc:`TokenError` upon an unexpected token
        '''
        # The stack will have contents after string concatenation.
        if self._token_stack:
            tok = self._token_stack.pop()
            self._tokens.append(tok)
            return tok

        # Everything after and including the cursor position:
        s = self._string[self._cursor:]

        # Match against each rule:
        for test, type_ in self._rules:
            m = re.match(test, s)

            if m is None:
                # This rule was not matched; try the next one.
                continue

            tok = Token(
                value=m.group(),
                at=(self._cursor, (self._lineno, self._colno)),
                type=type_,
                matchgroups=m.groups(),
                lexer=self,
                file=self._file
            )

            if type_ in TokGroup.T_Ignore:
                l = len(tok.value)
                self._cursor += l
                self._colno += l
                return (yield from self._get_token())

            # Update location:
            self._cursor += len(tok.value)
            self._colno += len(tok.value)
            if type_ is TokType.NEWLINE:
                self._lineno += len(tok.value)
                self._colno = 1

            if type_ is TokType.STRING:
                # Add to the string stack for error handling:
                self._string_debug = tok
                # Process strings by removing quotes:
                speech_char = tok.matchgroups[0]
                if speech_char in self.MULTILINE_QUOTES:
                    lines = tok.value.count(NEWLINE)
                    self._lineno += lines
                value = tok.value.strip(speech_char)
                if '\\' in value:
                    value = unescape_backslash(value)
                tok.value = value

                # Concatenate neighboring strings:
                if self.STRING_CONCAT:
                    while True:
                        maybe_str = (yield from self._get_token())
                        if maybe_str.type in TokGroup.T_Ignore:
                            continue
                        break

                    if maybe_str.type is TokType.STRING:
                        # Concatenate.
                        tok.value += maybe_str.value
                        self._tokens.append(tok)
                        return tok

                    else:
                        # Handle the next token separately.
                        self._token_stack.append(maybe_str)

                self._string_debug = None

            self._tokens.append(tok)
            return tok

        else:
            if s is self.eof:
                tok = Token(
                    value=s,
                    at=(self._cursor, (self._lineno, self._colno)),
                    type=TokType.ENDMARKER,
                    matchgroups=None,
                    lexer=self,
                    file=self._file
                )

                self._tokens.append(tok)
                return tok

            # If a token is not returned, prepare an error message:
            bad_value = s.split(None, 1)[0]
            bad_token = Token(
                value=bad_value,
                at=(self._cursor, (self._lineno, self._colno)),
                type=TokType.UNKNOWN,
                matchgroups=None,
                lexer=self,
                file=self._file
            )
            bad_toks = (bad_token,)

            if bad_value.startswith(self.SPEECH_CHARS):
                if self._string_debug is None:
                    # Broken single speech characters
                    msg = f"Unmatched quote:"
                    raise TokenError.hl_error(bad_toks, msg)

                # Broken triple speech characters
                msg = f"Unmatched multiline quote:"
                self._tokens.append(self._string_debug)

                # Two quotes of each kind:
                pairs = (s*2 for s in self.SPEECH_CHARS[:3])
                maybe_first_two = self._string_debug
                if maybe_first_two.match_repr in pairs:
                    # The current token is part of a multiline speech
                    # char begun by the previous token.
                    bad_toks = (maybe_first_two, bad_token)

            else:
                too_long = 8
                if len(bad_value) > too_long:
                    msg = f"Unexpected token:"
                else:
                    msg = f"Unexpected token: {bad_value!r}"

            self._tokens.append(bad_token)

            raise TokenError.hl_error(bad_toks, msg)


def unescape_backslash(s: str, encoding: str = 'utf-8') -> str:
    '''
    Unescape characters escaped by backslashes.

    :param s: The string to escape
    :type s: :class:`str`

    :param encoding: The encoding `s` comes in, defaults to ``'utf-8'``
    :type encoding: :class:`str`
    '''
    return (
        s.encode(encoding)
        .decode('unicode-escape')
        # .encode(encoding)
        # .decode(encoding)
    )


