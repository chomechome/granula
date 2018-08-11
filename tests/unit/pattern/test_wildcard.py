import fnmatch

import hypothesis

from granula.pattern import Wildcard

from tests.strategies import TEXT


@hypothesis.given(TEXT, TEXT)
def test_wildcard(filename, pattern):
    assert Wildcard(pattern).matches(filename) == fnmatch.fnmatch(filename, pattern)
