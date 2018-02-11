import hypothesis

from granula.pattern import Environment

from tests.strategies import WORD


@hypothesis.given(WORD, WORD, WORD)
@hypothesis.example('..config', 'testing', 'yaml')  # must ignore leading dots
def test_no_environment(name, environment, extension):
    filename = u'{}.{}'.format(name, extension)

    assert Environment(environment).matches(filename)


@hypothesis.given(WORD, WORD, WORD)
def test_environment(name, environment, extension):
    filename = u'{}.{}.{}'.format(name, environment, extension)

    assert Environment(environment).matches(filename)


@hypothesis.given(WORD, WORD, WORD, WORD)
def test_another_environment(name, environment, extension, another):
    hypothesis.assume(environment != another)
    filename = u'{}.{}.{}'.format(name, another, extension)

    assert not Environment(environment).matches(filename)
