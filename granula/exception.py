import os

from granula.pattern import IFilenamePattern


class ConfigNotFoundError(Exception):
    def __init__(self, directory, pattern, recursive):
        """
        :type directory: six.text_type
        :type pattern: IFilenamePattern
        :type recursive: bool
        """
        super(ConfigNotFoundError, self).__init__(
            u'No config files matching {pat} pattern {how}found under "{dir}"'
            .format(
                pat=pattern,
                how=u'recursively ' if recursive else u'',
                dir=os.path.abspath(directory),
            )
        )


class ConfigDataTypeError(Exception):
    def __init__(self, filename, datatype):
        """
        :type filename: six.text_type
        :type datatype: type
        """
        super(ConfigDataTypeError, self).__init__(
            u'Expected "{}" to contain a config mapping, got "{}" instead'
            .format(os.path.abspath(filename), datatype.__name__)
        )


class SerializerNameError(Exception):
    def __init__(self, expected, actual):
        """
        :type expected: collections.Iterable[six.text_type]
        :type actual: six.text_type
        """
        super(SerializerNameError, self).__init__(
            u'Unknown serializer name "{actual}", must be one of {expected}'
            .format(
                actual=actual,
                expected=u', '.join(u'"{}"'.format(name) for name in expected),
            )
        )


class ReferencePathError(Exception):
    def __init__(self, path):
        """
        :type path: collections.Iterable[six.text_type]
        """
        super(ReferencePathError, self).__init__(
            u'Config does not contain path {}'
            .format(u' -> '.join(u'"{}"'.format(step) for step in path))
        )


class EnvironmentVariableError(Exception):
    def __init__(self, variable):
        """
        :type variable: six.text_type
        """
        super(EnvironmentVariableError, self).__init__(
            u'Environment variable "{}" is not set'
            .format(variable)
        )


class ArgumentCountError(Exception):
    def __init__(self, count, min_count, max_count=None):
        """
        :type count: int
        :type min_count: int
        :type max_count: int
        """
        if min_count == max_count:
            arguments = u'exactly {}'.format(max_count)
        elif max_count is not None:
            arguments = u'from {} to {}'.format(min_count, max_count)
        else:
            arguments = u'at least {}'.format(min_count)

        super(ArgumentCountError, self).__init__(
            u'Expected {arguments} argument{plural}, {count} given'
            .format(
                arguments=arguments,
                count=count,
                plural=u's' if (max_count or min_count) != 1 else u'',
            )
        )
