import hypothesis.strategies

from granula.dsl.runner import run

from tests.strategies import DATA, TEXT
from tests.stubs.operator import Fail, Success
from tests.utils import assert_raises_dsl_error

# limit these to a reasonable interval, else RAM will explode
_COUNT = hypothesis.strategies.integers(min_value=1, max_value=1000)
_INDEX = hypothesis.strategies.integers(min_value=0, max_value=1000)


@hypothesis.given(_COUNT, _INDEX, DATA, DATA)
def test_success(operator_count, success_index, config, value):
    operators = [Fail() for _ in range(operator_count)]
    operators.insert(success_index, Success(value))

    assert run(enumerate(operators), config) == value


@hypothesis.given(_COUNT, DATA, TEXT)
def test_fail(operator_count, config, message):
    operators = [Fail(message) for _ in range(operator_count)]

    with assert_raises_dsl_error(message, position=operator_count - 1):
        run(enumerate(operators), config)


def test_no_dsl_operators():
    message = u'No DSL operators found'

    with assert_raises_dsl_error(message=message, position=0):
        run(operators=(), config={})
