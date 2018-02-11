import codecs

import six

from granula.dsl import defaults
from granula.dsl.exception import DSLError, DSLResolveError
from granula.dsl.finder import DSLFinder
from granula.dsl.parser import DSLParser
from granula.dsl.runner import run
from granula.operator import IOperator
from granula.serializer import ISerializer


class DSLResolver(object):
    """
    Processes a config file and resolves found DSL injections
    """
    def __init__(self, finder=None, operators=None):
        """
        :type finder: granula.dsl.finder.DSLFinder
        :type operators: collections.Mapping[six.text_type, type[IOperator]]
        """
        if finder is None:
            finder = DSLFinder()

        if operators is None:
            operators = defaults.OPERATORS

        self._finder = finder
        self._operators = operators

    def _resolve(self, dsl, config, serializer):
        """
        :type dsl: granula.dsl.finder.DSL
        :type config: collections.Mapping
        :rtype: six.text_type
        """
        parser = DSLParser(tokens=dsl.tokens, operators=self._operators)
        result = run(operators=parser.parse(), config=config)
        return serializer.serialize(result)

    def resolve(self, path, serializer, config, encoding=u'utf-8'):
        """
        Resolve all DSL injections in a given file
        :type path: six.text_type
        :type serializer: ISerializer
        :type config: collections.Mapping
        :type encoding: six.text_type
        :rtype: six.text_type
        :return: File contents with all the DSL injections resolved
        """
        with codecs.open(path, encoding=encoding) as stream:
            data = u''

            for line, source in enumerate(stream):
                position = 0
                try:
                    for dsl in self._finder.find(source):
                        data += source[position: dsl.start]
                        data += self._resolve(dsl, config, serializer)
                        position = dsl.end

                    data += source[position:]
                except DSLError as e:
                    error = DSLResolveError(
                        filename=path,
                        line=line,
                        position=position + e.position,
                        source=source,
                        exception=e,
                    )
                    six.raise_from(error, from_value=None)

            return data
