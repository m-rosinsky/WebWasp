import pkgutil
import sys

__all__ = [
    "__version__",
    "webwasp",
]

__version__ = (pkgutil.get_data(__package__, "VERSION") or b"").decode("ascii").strip()
version_info = tuple(int(v) if v.isdigit() else v for v in __version__.split("."))

if sys.version_info < (3, 7):
    print(f"WebWasp {__version__} requires Python 3.7+")
    sys.exit(1)

del sys
del pkgutil
