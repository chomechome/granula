import hypothesis.strategies
import pytest

from granula.exception import ReferencePathError
from granula.operator import Reference

from tests.strategies import TEXT, DATA

_PATH = hypothesis.strategies.lists(TEXT, min_size=1, average_size=10)
_LENGTH = hypothesis.strategies.integers(min_value=0, max_value=10)


def _get_config(path, value):
    """
    Create config where specified key path leads to value
    :type path: collections.Sequence[six.text_type]
    :type value: object
    :rtype: collections.Mapping
    """
    config = {}
    for step in reversed(path):
        config = {step: config or value}

    return config


@hypothesis.given(_PATH, DATA)
def test_reference(path, value):
    config = _get_config(path, value)

    assert Reference(*path).apply(config) == value


@hypothesis.given(_PATH, _LENGTH)
def test_reference_error(path, length):
    hypothesis.assume(length < len(path))

    config = _get_config(path[:length], value={})

    with pytest.raises(ReferencePathError):
        Reference(*path).apply(config)
