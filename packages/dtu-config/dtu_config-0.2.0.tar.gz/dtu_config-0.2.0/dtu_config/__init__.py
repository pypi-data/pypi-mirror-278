"""
dtu_config: <DESCRIPTION>
"""
import logging

from ._version import __version__
from .DTU_config import DtuConfig as DtuConfig

logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = ["__version__"]
