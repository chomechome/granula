import hypothesis

from granula.pattern import Extension

from tests.strategies import WORD


@hypothesis.given(WORD, WORD)
def test_no_extension(name, extension):
    assert not Extension(extension).matches(name)


@hypothesis.given(WORD, WORD)
def test_extension(name, extension):
    filename = u'{}.{}'.format(name, extension)

    assert Extension(extension).matches(filename)


@hypothesis.given(WORD, WORD, WORD)
def test_another_extension(name, extension, another):
    hypothesis.assume(extension != another)
    filename = u'{}.{}'.format(name, another)

    assert not Extension(extension).matches(filename)


@hypothesis.given(WORD, WORD, WORD)
def test_multiple_extensions(name, extension, another):
    filename = u'{}.{}.{}'.format(name, another, extension)

    assert Extension(extension).matches(filename)
