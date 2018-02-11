import collections

import enum
import six


class TokenType(six.text_type, enum.Enum):
    IDENTIFIER = 'identifier'
    STRING = 'string'
    INTEGER = 'integer'
    REAL = 'real'
    NULL = 'null'
    TRUE = 'true'
    FALSE = 'false'
    PIPE = 'pipe'


Token = collections.namedtuple('Token', 'position value type')
