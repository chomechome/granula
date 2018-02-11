import hypothesis.strategies
import pytest
import six

from granula.serializer import JSONSerializer
from tests.strategies import DATA


@pytest.fixture(name='serializer')
def _get_serializer():
    return JSONSerializer()


@hypothesis.given(DATA)
def test_round_trip(serializer, data):
    serialized = serializer.serialize(data)
    deserialized = serializer.deserialize(serialized)

    assert data == deserialized


@hypothesis.given(DATA)
def test_serialization_to_unicode(serializer, data):
    assert isinstance(serializer.serialize(data), six.text_type)
