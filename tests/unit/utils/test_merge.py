import hypothesis.strategies
import pytest

from granula.utils import merge

from tests.strategies import CONFIG


@hypothesis.given(CONFIG, CONFIG)
def test_merge_any_mappings(source, target):
    merge(source=source, target=target)


@pytest.mark.parametrize(
    ['target', 'source', 'expected'],
    [
        # add new value
        (
            {'one': 1},
            {'two': 2},
            {'one': 1, 'two': 2},
        ),
        (
            {'one': {'two': 1}},
            {'three': 2},
            {'one': {'two': 1}, 'three': 2},
        ),
        (
            {'one': {'two': 1}},
            {'one': {'three': 3}},
            {'one': {'two': 1, 'three': 3}},
        ),
        (
            {'one': {'two': {'three': 1}}},
            {'one': {'two': {'four': 2}}},
            {'one': {'two': {'three': 1, 'four': 2}}},
        ),
        (
            {'one': {'two': 1}},
            {'one': {'three': {'four': [1, 2, 3]}}},
            {'one': {'two': 1, 'three': {'four': [1, 2, 3]}}},
        ),

        # replace existing value
        (
            {'one': 1},
            {'one': 2},
            {'one': 2},
        ),
        (
            {'one': {'two': 1}},
            {'one': {'two': 2}},
            {'one': {'two': 2}},
        ),
        (
            {'one': {'two': {'three': 3}}},
            {'one': {'two': {'three': [3, 1, 3]}}},
            {'one': {'two': {'three': [3, 1, 3]}}},
        ),
    ]
)
def test_merge(target, source, expected):
    merge(source=source, target=target)

    assert target == expected
