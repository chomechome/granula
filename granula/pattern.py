import abc
import fnmatch
import os
import re

import six.moves


@six.add_metaclass(abc.ABCMeta)
class IFilenamePattern(object):
    @abc.abstractmethod
    def matches(self, filename):
        """
        Check whether a filename is matched by this pattern
        :type filename: six.text_type
        :rtype: bool
        """


@six.add_metaclass(abc.ABCMeta)
class CompositeFilenamePattern(IFilenamePattern):
    """
    Pattern that is based upon a number of other patterns
    """
    def __init__(self, *patterns):
        """
        :type patterns: IFilenamePattern
        """
        self._patterns = patterns

    def __repr__(self):
        return u'{type.__name__}({patterns})'.format(
            type=type(self),
            patterns=u', '.join(six.moves.map(repr, self._patterns)),
        )


class Any(CompositeFilenamePattern):
    """
    Match any of the underlying patterns
    """
    def matches(self, filename):
        return any(pattern.matches(filename) for pattern in self._patterns)


class All(CompositeFilenamePattern):
    """
    Match all of the underlying patterns
    """
    def matches(self, filename):
        return all(pattern.matches(filename) for pattern in self._patterns)


class Inverse(IFilenamePattern):
    """
    Pattern that matches everything not matched by the base pattern
    """
    def __init__(self, base):
        """
        :type base: IFilenamePattern
        """
        self._base = base

    def __repr__(self):
        return u'{type.__name__}({base})'.format(
            type=type(self),
            base=self._base,
        )

    def matches(self, filename):
        return not self._base.matches(filename)


class Environment(IFilenamePattern):
    """
    Special case environment filename pattern

    Example:
        >> pattern = Environment('development')
        >> pattern.matches('config.yaml')
        True
        >> pattern.matches('config.development.yaml')
        True
        >> pattern.matches('config.testing.yaml')
        False
        >> pattern.matches('config.production.yaml')
        False
    """
    def __init__(self, name):
        """
        :type name: six.text_type
        """
        self._name = name

    def __repr__(self):
        return u'{type.__name__}("{name}")'.format(
            type=type(self),
            name=self._name,
        )

    def matches(self, filename):
        stem, _ = os.path.splitext(filename)
        _, environment = os.path.splitext(stem)
        return not environment or self._name == environment.lstrip('.')


class Extension(IFilenamePattern):
    """
    Pattern that matches file extensions
    """
    def __init__(self, extension):
        """
        :type extension: six.text_type
        """
        self._extension = extension

    def __repr__(self):
        return u'{type.__name__}("{extension}")'.format(
            type=type(self),
            extension=self._extension,
        )

    def matches(self, filename):
        _, extension = os.path.splitext(filename)
        return self._extension == extension.lstrip('.')


class Wildcard(IFilenamePattern):
    """
    Shell-style wildcard filename pattern
    """
    def __init__(self, pattern):
        """
        :type pattern: six.text_type
        """
        self._pattern = pattern

    def __repr__(self):
        return u'{type.__name__}("{pattern}")'.format(
            type=type(self),
            pattern=self._pattern,
        )

    def matches(self, filename):
        return fnmatch.fnmatch(filename, self._pattern)


class Regex(IFilenamePattern):
    """
    Regular expression filename pattern
    """
    def __init__(self, pattern):
        """
        :type pattern: six.text_type
        """
        self._pattern = re.compile(pattern)

    def __repr__(self):
        return u'{type.__name__}("{pattern}")'.format(
            type=type(self),
            pattern=self._pattern,
        )

    def matches(self, filename):
        return bool(self._pattern.match(filename))
