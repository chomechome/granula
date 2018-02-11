import hypothesis.strategies
import os

from granula.utils import find_files

from tests.strategies import WORD
from tests.stubs.pattern import NoMatch
from tests.utils import create_temporary_directory

_FILENAMES = hypothesis.strategies.lists(
    elements=WORD,
    min_size=1,
    max_size=10,
    unique_by=lambda text: os.path.normcase(text),
)


def _create_files(directory, filenames):
    """
    :type directory: six.text_type
    :type filenames: six.text_type
    :rtype: list[six.text_type]
    """
    if not os.path.exists(directory):
        os.mkdir(directory)

    paths = sorted(os.path.join(directory, name) for name in filenames)
    for path in paths:
        open(path, mode='a').close()

    return paths


@hypothesis.given(_FILENAMES)
def test_non_recursive(filenames):
    with create_temporary_directory() as directory:
        paths = _create_files(directory, filenames)

        assert paths == find_files(directory, recursive=False)


@hypothesis.given(_FILENAMES, WORD)
def test_recursive(filenames, subdirectory):
    with create_temporary_directory() as directory:
        paths = _create_files(os.path.join(directory, subdirectory), filenames)

        assert paths == find_files(directory, recursive=True)


@hypothesis.given(_FILENAMES)
def test_pattern(filenames):
    with create_temporary_directory() as directory:
        _create_files(directory, filenames)

        assert not find_files(directory, pattern=NoMatch(), recursive=True)
