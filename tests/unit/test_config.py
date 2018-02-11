import pytest

from granula.config import Config

from tests.fixtures import get_fixture_path
from tests.stubs.serializer import CustomSerializer
from tests.utils import replace_environment


@pytest.mark.parametrize(
    ['serializer', 'directory', 'environment', 'expected'],
    [
        (
            'yaml',
            'config/yaml',
            {
                'VARIABLE': 'variable',
                'FIRST': 'first',
            },
            {
                'parameters': {
                    'default': 10,
                    'nested': 'extended',
                    'environment': 'variable',
                    'reference': 'value',
                },
                'new': 'value',
                'list': [
                    'first',
                    'string',
                ],
            }
        ),
        (
            'json',
            'config/json',
            {
                'SECRET': 'secret',
                'ONE': 'one',
            },
            {
                'list': [
                    'one',
                    'two',
                ],
                'default': 15,
                'parameters': {
                    'nested': 'extended',
                    'reference': 'value',
                    'variable': 'secret',
                },
            },
        ),
        (
            CustomSerializer(),
            'config/custom',
            {
                'SECRET': 'secret',
            },
            {
                'DEFAULT': 'extended',
                'ENVIRONMENT': 'secret',
                'MISS': '10',
                'NEW': 'value',
                'REFERENCE': '10',
            },
        ),
    ]
)
def test_from_directory(serializer, directory, environment, expected):
    path = get_fixture_path(directory)
    with replace_environment(variables=environment):
        config = Config.from_directory(directory=path, serializer=serializer)

    assert config == expected


def test_from_file():
    pass
