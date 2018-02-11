import re

from granula.dsl.exception import DSLError
from granula.dsl.token import Token, TokenType

_CONVERTERS = {
    TokenType.REAL: float,
    TokenType.INTEGER: int,
    TokenType.NULL: lambda _: None,
    TokenType.TRUE: lambda _: True,
    TokenType.FALSE: lambda _: False,
    TokenType.STRING: lambda string: string[1:-1],  # strip quotes
}
_TOKEN = re.compile(
    '|'.join(
        '(?P<{}>{})'.format(token, regex) for token, regex in [
            (TokenType.PIPE, r'\|'),
            (TokenType.REAL, r'(\B-)?\b\d+(\.\d+|(\.\d+)?e[-+]?\d+)\b'),
            (TokenType.INTEGER, r'(\B-)?\b\d+\b'),
            (TokenType.NULL, r'\b[Nn]one|[Nn]ull\b'),
            (TokenType.TRUE, r'[Tt]rue'),
            (TokenType.FALSE, r'[Ff]alse'),
            (TokenType.IDENTIFIER, r'[^\W\d_]\w*'),
            (TokenType.STRING, r'\"[^\"]*\"|\'[^\']*\''),
        ]
    )
)
_WHITESPACE = re.compile(r'\s+')


def _get_token(match):
    """
    :type match: re.Match
    :rtype: Token
    """
    token_type = TokenType(match.lastgroup)
    value = match.group(token_type)

    converter = _CONVERTERS.get(token_type)
    if converter is not None:
        value = converter(value)

    return Token(
        position=match.start(),
        type=token_type,
        value=value,
    )


def scan(source, position=0, breakpoint=r'$'):
    """
    Scan DSL source for tokens from position to first breakpoint match
    :type source: six.text_type
    :type position: int
    :type breakpoint: six.text_type
    :rtype: tuple[int, list[Token]]
    :return: Breakpoint match end and a list of tokens
    """
    breakpoint = re.compile(breakpoint)

    tokens = []
    while True:
        match = breakpoint.match(source, pos=position)
        if match is not None:
            return match.end(), tokens

        match = _WHITESPACE.match(source, pos=position)
        if match is None:
            match = _TOKEN.match(source, pos=position)
            if match is None:
                break

            tokens.append(_get_token(match))

        position = match.end()

    if position < len(source):
        msg = u'Unexpected symbol "{}"'.format(source[position])
    else:
        msg = u'Expected to match regex "{}"'.format(breakpoint.pattern)

    raise DSLError(message=msg, position=position)
