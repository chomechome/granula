import pytest
import six

from granula.exception import ArgumentCountError
from granula.utils import check_argument_count


def _assert_raises_argument_count_error(func, count, message):
    with pytest.raises(ArgumentCountError) as context:
        check_argument_count(func, count)

    assert six.text_type(context.value) == message


def test_too_few_arguments():
    _assert_raises_argument_count_error(
        message=u'Expected exactly 3 arguments, 2 given',
        func=lambda a, b, c: None,
        count=2,
    )


def test_too_many_arguments():
    _assert_raises_argument_count_error(
        message=u'Expected exactly 2 arguments, 3 given',
        func=lambda a, b: None,
        count=3,
    )


def test_default_arguments():
    _assert_raises_argument_count_error(
        message=u'Expected from 1 to 2 arguments, 3 given',
        func=lambda a, b=1: None,
        count=3,
    )


def test_single_argument():
    _assert_raises_argument_count_error(
        message=u'Expected exactly 1 argument, 2 given',
        func=lambda a: None,
        count=2,
    )


def test_single_default_argument():
    _assert_raises_argument_count_error(
        message=u'Expected from 0 to 1 argument, 2 given',
        func=lambda a=1: None,
        count=2,
    )


def test_any_number_of_arguments():
    _assert_raises_argument_count_error(
        message=u'Expected at least 1 argument, 0 given',
        func=lambda a, *b: None,
        count=0,
    )


def test_zero_arguments():
    _assert_raises_argument_count_error(
        message=u'Expected exactly 0 arguments, 1 given',
        func=lambda: None,
        count=1,
    )
