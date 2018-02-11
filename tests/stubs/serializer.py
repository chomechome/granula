import collections

import six

from granula.serializer import ISerializer


class CustomSerializer(ISerializer):
    def serialize(self, data):
        if not isinstance(data, collections.Mapping):
            return six.text_type(data)
        return u'\n'.join(u'{}={}'.format(key, value)
                          for key, value in six.iteritems(data))

    def deserialize(self, data):
        result = {}
        for line in data.splitlines():
            key, value = line.split('=')
            result[key] = value

        return result
