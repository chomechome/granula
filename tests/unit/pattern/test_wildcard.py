import fnmatch

import hypothesis

from granula.pattern import Wildcard

from tests.strategies import TEXT


@hypothesis.given(TEXT, TEXT)
def test_wildcard(filename, pattern):
    wildcard = Wildcard(pattern)

    assert wildcard.matches(filename) == fnmatch.fnmatch(filename, pattern)
