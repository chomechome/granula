from granula.dsl.exception import DSLError
from granula.operator import IOperator


def run(operators, config):
    """
    Apply DSL operators to config and return first successful result
    :type operators: collections.Iterable[tuple[int, IOperator]]
    :type config: collections.Mapping
    :rtype: object
    """
    last_error = None
    last_error_position = 0

    for position, operator in operators:
        try:
            return operator.apply(config)
        except Exception as e:
            last_error = e
            last_error_position = position

    message = u'No DSL operators found' if last_error is None else last_error
    raise DSLError(message, position=last_error_position)
