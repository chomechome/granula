import re

from granula.operator import Reference, EnvironmentVariable, Value

OPERATORS = {
    u'ref': Reference,
    u'env': EnvironmentVariable,
    u'val': Value,
}
PREFIX = re.escape(u'${')
SUFFIX = re.escape(u'}')
