from .token import Token, TokType, TokGroup


class ConfigError(SyntaxError):
    '''
    Base exception for errors related to config file parsing.
    '''
    pass


class TokenError(ConfigError):
    '''
    An exception affecting individual tokens and their arrangement.
    '''
    def __init__(self, msg: str, *args, **kwargs) -> None:
        super().__init__(self)
        # Replicate the look of natural SyntaxError messages:
        self.msg = '\n' + msg

    @classmethod
    def hl_error(
        cls,
        tokens: Token | tuple[Token],
        msg: str,
        with_col: bool = True,
        leader: str = None,
        indent: int = 2
    ):
        '''
        Highlight the part of a line occupied by a token.
        Return the original line surrounded by quotation marks followed
        by a line of spaces and arrows that point to the token.

        :param tokens: The token or tokens to be highlighted
        :type tokens: :class:`Token` | tuple[:class:`Token`]

        :param msg: The error message to display after `leader`
            column number
        :type msg: :class:`str`

        :param with_col: Display the column number of the token,
            defaults to ``True``
        :type with_col: :class:`bool`
        
        :param leader: The error leader to use,
            defaults to that of the first token
        :type leader: :class:`str`

        :param indent: Indent by this many spaces * 2,
            defaults to 2
        :type indent: :class:`int`

        :returns: A new :class:`TokenError` with a custom error message
        :rtype: :class:`TokenError`
        '''
        if isinstance(tokens, Token):
            tokens = (tokens,)

        first_tok = tokens[0]
        lexer = first_tok.lexer
        if leader is None:
            leader = first_tok.error_leader()

        if indent is None:
            indent = 0
        dent = ' ' * indent

        max_len = 100
        break_line = "\n" + dent if len(leader + msg) > max_len else ""
        dent = 2 * dent  # Double indent for following lines.
        highlight = ""

        if len(tokens) == 1:
            line_bridge = " "
            line = lexer.get_line(first_tok)
            if first_tok.type is TokType.STRING:
                text = first_tok.match_repr
            else:
                text = first_tok.value
            between = tokens

        else:
            # Highlight multiple tokens using all in the range:
            line_bridge = " "
            between = lexer.in_range(tokens[0], tokens[-1])
            if not between:
                between = tokens
            if any(t.type is TokType.NEWLINE for t in between):
                # Consolidate multiple lines:
                with_dups = (
                    lexer.get_line(t) for t in between
                    if t.type not in TokGroup.T_Ignore
                )
                lines = dict.fromkeys(with_dups)
                # Don't count line breaks twice:
                lines.pop('', None)
                line = line_bridge.join(lines)
            else:
                line = lexer.get_line(first_tok)

        # Work out the highlight line:
        for t in between:
            token_length = len(t.value)
            type_ = t.type
            if type_ in (*TokGroup.T_Ignore, TokType.NEWLINE, TokType.ENDMARKER):
                if t is between[-1]:
                    token_length = 0
            match type_:
                case TokType.STRING:
                    # match_repr contains the quotation marks:
                    token_length = len(t.match_repr)
                case TokType.UNKNOWN:
                    token_length = 1
                case _:
                    pass

            highlight += '^' * token_length

        # Determine how far along the first token is in the line:
        line_start = len(line) - len(line.lstrip())
        if between[-1].type is TokType.NEWLINE:
            line_end = len(line) - len(line.rstrip())
            line_start += line_end
        tok_start_distance = first_tok.colno - line_start - 1
        offset = ' ' * tok_start_distance
        highlight = dent + offset + highlight
        line = dent + line.strip()

        errmsg = leader + break_line + msg + '\n'.join(('', line, highlight))
        return cls(errmsg)


class ParseError(TokenError):
    '''
    Exception raised during parsing operations.
    '''
    pass


class CompileError(TokenError):
    '''
    Exception raised during compiling operations.
    '''
    pass


