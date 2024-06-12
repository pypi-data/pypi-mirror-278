# read version from installed package
from importlib.metadata import version

__version__ = version("paradigma")

from .dummy import (
    hello_world
)
