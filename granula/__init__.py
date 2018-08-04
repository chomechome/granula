from .config import Config
from .dsl import DSLResolver, DSLFinder
from .pattern import Any, All, Inverse, Environment, Extension, Wildcard, Regex
from .serializer import YAMLSerializer, JSONSerializer

from_directory = Config.from_directory
from_files = Config.from_files
from_path = Config.from_path

__version__ = '2018.02.8'
