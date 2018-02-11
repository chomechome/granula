import abc
import os

import six

from granula.exception import ReferencePathError, EnvironmentVariableError


@six.add_metaclass(abc.ABCMeta)
class IOperator(object):
    @abc.abstractmethod
    def apply(self, config):
        """
        :type config: collections.Mapping
        :rtype: object
        """


class Value(IOperator):
    def __init__(self, value):
        """
        :type value: object
        """
        self._value = value

    def apply(self, config):
        return self._value


class Reference(IOperator):
    def __init__(self, start, *path):
        """
        :type path: collections.Sequence[six.text_type]
        """
        self._path = (start,) + path

    def apply(self, config):
        for step in self._path:
            if step not in config:
                raise ReferencePathError(self._path)
            config = config[step]

        return config


class EnvironmentVariable(IOperator):
    def __init__(self, name):
        """
        :type name: six.text_type
        """
        self._name = name

    def apply(self, config):
        value = os.getenv(self._name)
        if value is None:
            raise EnvironmentVariableError(self._name)

        return value
