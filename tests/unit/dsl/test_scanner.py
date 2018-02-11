import re

import hypothesis.strategies
import pytest

from granula.dsl.scanner import scan
from granula.dsl.token import Token, TokenType

from tests.strategies import WORD
from tests.utils import assert_raises_dsl_error

_WHITESPACE = hypothesis.strategies.from_regex(r'^\s+$')
_BREAKPOINT = hypothesis.strategies.from_regex(r'^[^\s\w]+$')


def _assert_tokens_match(source, expected):
    """
    :type source: six.text_type
    :type expected: collections.Sequence[Token]
    """
    position, actual = scan(source)

    assert expected == actual
    assert position == len(source)


def _assert_token_matches(source, value, token_type):
    """
    :type source: six.text_type
    :type value: object
    :type token_type: TokenType
    """
    _assert_tokens_match(
        source=source,
        expected=[Token(position=0, value=value, type=token_type)],
    )


def test_pipe():
    _assert_token_matches(source=u'|', value=u'|', token_type=TokenType.PIPE)


@pytest.mark.parametrize(
    'source',
    [
        u'1.1',
        u'-1.1',
        u'52115.87857645321',
        u'-1.000000000000000001',
        u'2e1',
        u'2e+1',
        u'2e-1',
        u'15.1456e+10',
        u'12.5151241e-5',
    ]
)
def test_real(source):
    _assert_token_matches(
        source=source,
        value=float(source),
        token_type=TokenType.REAL,
    )


@pytest.mark.parametrize(
    'source',
    [
        u'1',
        u'0',
        u'-1',
        u'9518284859421',
        u'-125125666551',
    ]
)
def test_integer(source):
    _assert_token_matches(
        source=source,
        value=int(source),
        token_type=TokenType.INTEGER,
    )


@pytest.mark.parametrize('source', [u'None', u'none', u'Null', u'null'])
def test_null(source):
    _assert_token_matches(source, value=None, token_type=TokenType.NULL)


@pytest.mark.parametrize('source', [u'True', u'true'])
def test_true(source):
    _assert_token_matches(source, value=True, token_type=TokenType.TRUE)


@pytest.mark.parametrize('source', [u'False', u'false'])
def test_false(source):
    _assert_token_matches(source, value=False, token_type=TokenType.FALSE)


@pytest.mark.parametrize(
    ['source', 'value'],
    [
        (u'abc', u'abc'),
        (u'say_hi_to_underscores', u'say_hi_to_underscores'),
        (u'numbers123', u'numbers123'),
    ]
)
def test_identifier(source, value):
    _assert_token_matches(source, value, token_type=TokenType.IDENTIFIER)


@pytest.mark.parametrize(
    ['source', 'value'],
    [
        (u'"string string string"', u'string string string'),
        (u'"http://this.is.url"', u'http://this.is.url'),
        (u'\'some whitespaces here\'', u'some whitespaces here'),
    ]
)
def test_string(source, value):
    _assert_token_matches(source, value, token_type=TokenType.STRING)


@pytest.mark.parametrize(
    ['source', 'token', 'position'],
    [
        (u'text-12.5', u'-', 4),
        (u'abc-12', u'-', 3),
        (u'awesome+5', u'+', 7),
        (u'caramba!', u'!', 7),
        (u'# is not allowed', u'#', 0),
        (u'operator: value', u':', 8),
        (u'd.o.t.s', u'.', 1),
        (u'.no.dots.', u'.', 0),
        (u'0abc', u'0', 0),
        (u'_text', u'_', 0),
    ]
)
def test_unexpected_symbol(source, token, position):
    message = u'Unexpected symbol "{}"'.format(token)
    with assert_raises_dsl_error(message, position):
        scan(source)


def test_many():
    _assert_tokens_match(
        source=u'first one two|second 10|third none',
        expected=[
            Token(position=0, value=u'first', type=TokenType.IDENTIFIER),
            Token(position=6, value=u'one', type=TokenType.IDENTIFIER),
            Token(position=10, value=u'two', type=TokenType.IDENTIFIER),
            Token(position=13, value=u'|', type=TokenType.PIPE),
            Token(position=14, value=u'second', type=TokenType.IDENTIFIER),
            Token(position=21, value=10, type=TokenType.INTEGER),
            Token(position=23, value=u'|', type=TokenType.PIPE),
            Token(position=24, value=u'third', type=TokenType.IDENTIFIER),
            Token(position=30, value=None, type=TokenType.NULL),
        ]
    )


@hypothesis.given(WORD, WORD, _WHITESPACE)
def test_position(left, right, whitespace):
    source = left + whitespace + right
    position, tokens = scan(source=source, position=len(left))

    assert tokens == [
        Token(
            position=len(left) + len(whitespace),
            value=right,
            type=TokenType.IDENTIFIER,
        ),
    ]
    assert position == len(source)


@hypothesis.given(WORD, WORD, _WHITESPACE, _BREAKPOINT)
def test_breakpoint(left, right, whitespace, breakpoint):
    source = left + whitespace + breakpoint + whitespace + right
    position, tokens = scan(source=source, breakpoint=re.escape(breakpoint))

    assert tokens == [Token(position=0, value=left, type=TokenType.IDENTIFIER)]
    assert position == len(left) + len(whitespace) + len(breakpoint)
