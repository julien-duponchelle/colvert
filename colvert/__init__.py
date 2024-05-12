# When installed via pip a version.py file is created in the package directory
# for local development the version does not exist and is set to 'dev'
try:
    from ._version import (  # type: ignore
        __version__,
        __version_tuple__,
        version,
        version_tuple,
    )
except ModuleNotFoundError:
    __version__ = version = 'dev'
    __version_tuple__ = version_tuple = (0, 0, 0)

