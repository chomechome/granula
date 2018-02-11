import collections
import inspect
import os

import six

from granula.exception import ArgumentCountError
from granula.pattern import IFilenamePattern, Wildcard


def find_files(directory, pattern=Wildcard('*'), recursive=False):
    """
    Find file paths under a directory that match a given text pattern
    :type directory: six.string_types
    :type pattern: IFilenamePattern
    :type recursive: bool
    :rtype: list[six.string_types]
    :return: Lexicographically sorted absolute file paths
    """
    files = []

    for directory, _, filenames in os.walk(directory):
        for filename in filenames:
            if pattern.matches(filename):
                files.append(os.path.join(directory, filename))

        if not recursive:
            break

    return sorted(files)


def merge(source, target):
    """
    :type source: collections.Mapping
    :type target: collections.MutableMapping
    """
    for key, value in six.iteritems(source):
        if (isinstance(target.get(key), collections.MutableMapping) and
                isinstance(value, collections.Mapping)):
            merge(source=value, target=target[key])
        else:
            target[key] = value


def check_argument_count(func, count):
    """
    Check that `func` takes `count` arguments
    :type func: function
    :type count: int
    :raises ArgumentCountError
    """
    get_signature = inspect.getargspec if six.PY2 else inspect.getfullargspec
    signature = get_signature(func)

    max_count = len(signature.args) - int('self' in signature.args)
    min_count = max_count - len(signature.defaults or ())

    if signature.varargs:
        max_count = None

    if min_count > count or (max_count is not None and max_count < count):
        raise ArgumentCountError(count, min_count, max_count)
