from granula.operator import IOperator


class Fail(IOperator):
    def __init__(self, message=u''):
        self._message = message

    def apply(self, config):
        raise ValueError(self._message)


class Success(IOperator):
    def __init__(self, value):
        self._value = value

    def apply(self, config):
        return self._value
