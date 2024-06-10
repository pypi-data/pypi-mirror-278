"""
\u0420\u0430\u0437\u0440\u0430\u0431\u043E\u0442\u0447\u0438\u043A: MainPlay TG
https://t.me/MainPlay_InfoCh"""

__version_tuple__ = (0, 0, 12)
__depends__ = {"required": ["MainShortcuts", "flask", "requests"], "optional": []}
__scripts__ = ["MSVC-server", "MSVC-client"]
from .api import Launcher
__all__ = ["Launcher"]
__all__.sort()
__version__ = "{}.{}.{}".format(*__version_tuple__)
