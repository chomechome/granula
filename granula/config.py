import collections

import attrdict
import six

from granula.dsl import DSLResolver
from granula.exception import ConfigNotFoundError, ConfigDataTypeError
from granula.factory import get_serializer
from granula.pattern import Wildcard
from granula.serializer import ISerializer
from granula.utils import find_files, merge


class Config(attrdict.AttrMap):
    @classmethod
    def from_files(cls,
                   files,
                   encoding='utf-8',
                   serializer='yaml',
                   resolver=None,
                   default=None,
                   ):
        """
        Create a single config from contents of multiple files
        :type files: collections.Iterable[six.text_type|six.string_type]
        :type encoding: six.string_types
        :type serializer: ISerializer|six.text_type|six.binary_type
        :type resolver: DSLResolver
        :type default: collections.Mapping
        :rtype: Config
        """
        if isinstance(serializer, six.string_types):
            serializer = get_serializer(serializer)

        if resolver is None:
            resolver = DSLResolver()

        config = cls(default)
        for path in files:
            content = resolver.resolve(path, serializer, config, encoding)

            data = serializer.deserialize(content)
            if not isinstance(data, collections.Mapping):
                raise ConfigDataTypeError(path, datatype=type(data))

            merge(source=data, target=config)

        return config

    @classmethod
    def from_path(cls,
                  path,
                  encoding='utf-8',
                  serializer='yaml',
                  resolver=None,
                  default=None,
                  ):
        """
        Create config from a single file
        :type path: six.text_type|six.string_type
        :type encoding: six.string_types
        :type serializer: ISerializer|six.text_type|six.binary_type
        :type resolver: DSLResolver
        :type default: collections.Mapping
        :rtype: Config
        """
        return cls.from_files(
            files=[path],
            encoding=encoding,
            serializer=serializer,
            resolver=resolver,
            default=default,
        )

    @classmethod
    def from_directory(cls,
                       directory,
                       pattern='*',
                       encoding='utf-8',
                       serializer='yaml',
                       resolver=None,
                       default=None,
                       recursive=False,
                       ):
        """
        Create config from files in a directory that match a regex pattern
        :type directory: six.text_type|six.string_type
        :type pattern: six.text_type|six.string_type
        :type encoding: six.string_types
        :type serializer: ISerializer|six.text_type|six.binary_type
        :type resolver: DSLResolver
        :type default: collections.Mapping
        :type recursive: bool
        :rtype: Config
        """
        if isinstance(pattern, six.string_types):
            pattern = Wildcard(pattern)

        files = find_files(directory, pattern, recursive)
        if not files:
            raise ConfigNotFoundError(directory, pattern, recursive)

        return cls.from_files(
            files=files,
            encoding=encoding,
            serializer=serializer,
            resolver=resolver,
            default=default,
        )

    def __repr__(self):
        return u'{type.__name__}({attributes})'.format(
            type=type(self),
            attributes=repr(self._mapping),
        )
