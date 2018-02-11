from granula.exception import SerializerNameError
from granula.serializer import ISerializer, YAMLSerializer, JSONSerializer

_SERIALIZERS = {
    u'yaml': YAMLSerializer,
    u'json': JSONSerializer,
}


def get_serializer(name):
    """
    :type name: six.text_type|six.binary_type
    :rtype: ISerializer
    """
    if name not in _SERIALIZERS:
        raise SerializerNameError(expected=_SERIALIZERS, actual=name)

    return _SERIALIZERS[name]()
