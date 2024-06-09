from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("brd_serp_client")
except PackageNotFoundError:
    # package is not installed
    pass

from .client import GoogleSearchAPI
