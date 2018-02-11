import hypothesis.strategies

from granula.dsl.parser import DSLParser
from granula.dsl.token import Token, TokenType

from tests.strategies import TEXT, INTEGER
from tests.utils import assert_raises_dsl_error

_TOKEN_TYPE = hypothesis.strategies.sampled_from(TokenType)


@hypothesis.given(TEXT, INTEGER, _TOKEN_TYPE)
def test_expected_dsl_operator_name(value, position, token_type):
    hypothesis.assume(token_type is not TokenType.IDENTIFIER)

    parser = DSLParser(
        tokens=[Token(position=position, value=value, type=token_type)],
        operators={},
    )

    message = u'Expected DSL operator name'
    with assert_raises_dsl_error(message, position):
        parser.parse()


@hypothesis.given(TEXT, INTEGER)
def test_unknown_operator(name, position):
    parser = DSLParser(
        [Token(position=position, value=name, type=TokenType.IDENTIFIER)],
        operators={},
    )

    message = u'Unknown operator "{}"'.format(name)
    with assert_raises_dsl_error(message, position):
        parser.parse()
