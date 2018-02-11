import six

from granula.dsl.exception import DSLError
from granula.dsl.token import TokenType
from granula.exception import ArgumentCountError
from granula.operator import IOperator
from granula.utils import check_argument_count


class DSLParser(object):
    """
    Parses tokens into a sequence of DSL operators
    """
    def __init__(self, tokens, operators):
        """
        :type tokens: collections.Sequence[Token]
        :type operators: collections.Mapping[six.text_type, type[IOperator]]
        """
        self._tokens = tokens
        self._operators = operators

        self._current = 0

    def _is_end_of_file(self):
        """
        :rtype: bool
        """
        return self._current >= len(self._tokens)

    def _advance(self):
        """
        :rtype: Token
        """
        cursor = self._tokens[self._current]
        self._current += 1
        return cursor

    def _get_operator_type(self, token):
        """
        :type token: Token
        :rtype: type[IOperator]
        """
        if token.type is not TokenType.IDENTIFIER:
            message = u'Expected DSL operator name'
            raise DSLError(message, token.position)

        operator = self._operators.get(token.value)
        if operator is None:
            message = u'Unknown operator "{}"'.format(token.value)
            raise DSLError(message, token.position)

        return operator

    def _get_arguments(self):
        """
        :rtype: list[object]
        """
        arguments = []

        while not self._is_end_of_file():
            cursor = self._advance()
            if cursor.type is TokenType.PIPE:
                break

            arguments.append(cursor.value)

        return arguments

    def _iter_operators(self):
        """
        :rtype: collections.Iterable[tuple[int, IOperator]]
        """
        while not self._is_end_of_file():
            cursor = self._advance()
            operator = self._get_operator_type(cursor)
            arguments = self._get_arguments()

            try:
                check_argument_count(operator.__init__, count=len(arguments))
            except ArgumentCountError as e:
                error = DSLError(message=e, position=cursor.position)
                six.raise_from(error, from_value=None)

            yield cursor.position, operator(*arguments)

    def parse(self):
        """
        Parse tokens and produce corresponding operators with their positions
        :rtype: list[tuple[int, IOperator]]
        :return: Position and operator pairs
        """
        return list(self._iter_operators())
