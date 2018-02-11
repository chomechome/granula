import abc
import json

import six
import yaml


@six.add_metaclass(abc.ABCMeta)
class ISerializer(object):
    """
    Deserializes text into arbitrary Python objects and serializes them back
    """
    @abc.abstractmethod
    def serialize(self, data):
        """
        :type data: object
        :rtype: six.text_type
        """

    @abc.abstractmethod
    def deserialize(self, data):
        """
        :type data: six.text_type
        :rtype: object
        """


class YAMLSerializer(ISerializer):
    def __init__(self, loader=yaml.SafeLoader, dumper=yaml.SafeDumper):
        """
        :type loader: type[yaml.Loader]
        :type dumper: type[yaml.Dumper]
        """
        self._loader = loader
        self._dumper = dumper

    def serialize(self, data):
        result = yaml.dump(data, Dumper=self._dumper, allow_unicode=True)

        # python2 workaround
        if isinstance(result, six.binary_type):
            result = result.decode('utf-8')

        # PyYAML adds <document end> tag if it is not present already
        # we want to remove those so that we can partially serialize documents
        if result.endswith('...\n'):
            result = result[:-4]

        return result

    def deserialize(self, data):
        return yaml.load(data, Loader=self._loader)


class JSONSerializer(ISerializer):
    def __init__(self, encoder=None, decoder=None):
        """
        :type encoder: json.JSONEncoder
        :type decoder: json.JSONDecoder
        """
        self._encoder = encoder or json.JSONEncoder(ensure_ascii=False)
        self._decoder = decoder or json.JSONDecoder()

    def serialize(self, data):
        result = self._encoder.encode(data)

        # python2 workaround
        if isinstance(result, six.binary_type):
            result = result.decode(self._encoder.encoding)

        return result

    def deserialize(self, data):
        return self._decoder.decode(data)
