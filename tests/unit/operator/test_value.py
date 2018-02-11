import hypothesis

from granula.operator import Value
from tests.strategies import CONFIG, DATA


@hypothesis.given(CONFIG, DATA)
def test_return_value(config, value):
    assert Value(value).apply(config) == value
