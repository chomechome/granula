import contextlib
import os
import shutil
import tempfile

import pytest
import six

from granula.dsl.exception import DSLError


@contextlib.contextmanager
def replace_environment(variables):
    """
    :type variables: dict[six.text_type, six.text_type]
    """
    backup = os.environ.copy()

    os.environ.clear()
    os.environ.update(variables)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(backup)


@contextlib.contextmanager
def remove_from_environment(name):
    """
    :type name: six.text_type
    """
    backup = os.environ.pop(name, None)
    try:
        yield
    finally:
        if backup is not None:
            os.environ[name] = backup


@contextlib.contextmanager
def assert_raises_dsl_error(message=None, position=None):
    """
    :type message: six.text_type
    :type position: int
    """
    with pytest.raises(DSLError) as context:
        yield

    exception = context.value

    if message is not None:
        assert six.text_type(exception) == message

    if position is not None:
        assert exception.position == position


@contextlib.contextmanager
def create_temporary_directory():
    """
    :return: Temporary directory path
    :rtype: six.text_type
    """
    path = tempfile.mkdtemp()
    try:
        yield path
    finally:
        shutil.rmtree(path)
