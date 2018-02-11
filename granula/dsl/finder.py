import collections
import re

from granula.dsl import defaults
from granula.dsl.scanner import scan

DSL = collections.namedtuple(u'DSL', u'start end tokens')


class DSLFinder(object):
    """
    Finds DSL injections in a text
    """
    def __init__(self, prefix=None, suffix=None):
        """
        :type prefix: six.text_type
        :type suffix: six.text_type
        """
        self._prefix = re.compile(prefix or defaults.PREFIX)
        self._suffix = re.compile(suffix or defaults.SUFFIX)

    def _iter_dsl(self, source):
        """
        :type source: six.text_type
        :rtype: collections.Iterable[DSL]
        """
        position = 0

        while True:
            prefix = self._prefix.search(source, pos=position)
            if prefix is None:
                break

            position, tokens = scan(
                source=source,
                position=prefix.end(),
                breakpoint=self._suffix,
            )
            yield DSL(
                start=prefix.start(),
                end=position,
                tokens=tokens,
            )

    def find(self, source):
        """
        Find DSL injections in a source and return corresponding DSL objects
        :type source: six.text_type
        :rtype: list[DSL]
        :return: Objects that contain DSL tokens and position
        """
        return list(self._iter_dsl(source))
