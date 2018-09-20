from .client import Pulsedive
from .exceptions import PulsediveException

VERSION = (0, 0, 2)
__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))