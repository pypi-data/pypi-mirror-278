import logging
from collections import namedtuple

from .exception_util import exception_as_string
from .conditional_sleep import sleep_with_condition

__all__ = ("exception_as_string", "async_util", "caching", 'sleep_with_condition')
__version__ = "1.2.0"
VersionInfo = namedtuple("VersionInfo", "major minor micro releaselevel serial")
version_info = VersionInfo(major=1, minor=1, micro=0, releaselevel="final", serial=0)
logging.getLogger(__name__).addHandler(logging.NullHandler())
