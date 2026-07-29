from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("tempyenv")
except PackageNotFoundError:
    __version__ = "unknown"

__author__ = "David Whiteside"
