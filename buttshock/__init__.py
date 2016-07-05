from .base import ButtshockET312Base, ButtshockError
from .emulator import ButtshockET312Emulator, ButtshockET312EmulatorSync, ButtshockET312SerialEmulator

try:
    from .comm import ButtshockET312SerialSync
except:
    pass

__version__ = '0.1.0'

VERSION = __version__
