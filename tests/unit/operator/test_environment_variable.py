import hypothesis.strategies
import pytest
import six

from granula.exception import EnvironmentVariableError
from granula.operator import EnvironmentVariable

from tests.strategies import CONFIG, TEXT, WORD
from tests.utils import replace_environment, remove_from_environment


@hypothesis.given(CONFIG, WORD, TEXT)
def test_environment_variable(config, name, value):
    value = value.replace(u'\0', u'\\0')
    if six.PY2:
        # python2 environ does not allow unicode values
        value = value.encode('utf8')

    with replace_environment(variables={name: value}):
        assert EnvironmentVariable(name).apply(config) == value


@hypothesis.given(CONFIG, WORD)
def test_environment_variable_not_set(config, name):
    with remove_from_environment(name):
        with pytest.raises(EnvironmentVariableError) as context:
            EnvironmentVariable(name).apply(config)

        message = u'Environment variable "{}" is not set'.format(name)
        assert six.text_type(context.value) == message
