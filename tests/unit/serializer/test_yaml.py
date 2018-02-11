import hypothesis
import pytest
import six

from granula.serializer import YAMLSerializer
from tests.strategies import DATA, LITERAL


@pytest.fixture(name='serializer')
def _get_serializer():
    return YAMLSerializer()


@hypothesis.given(DATA)
def test_round_trip(serializer, data):
    serialized = serializer.serialize(data)
    deserialized = serializer.deserialize(serialized)

    assert data == deserialized


@hypothesis.given(DATA)
def test_serialization_to_unicode(serializer, data):
    assert isinstance(serializer.serialize(data), six.text_type)


@hypothesis.given(LITERAL)
def test_partial_serialization(serializer, literal):
    serialized = serializer.serialize(literal)

    assert not serialized.endswith('...\n')
