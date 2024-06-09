"""
ByMaNiM: A python packages for creating manim video and slides
================================================================



Subpackages
-----------
Using any of these subpackages requires an explicit import. For example,
``import bymanim.components``.

::

 components                   --- Components for Manim Video/Slides
 slides                        --- Standard Manim Slide

"""

import importlib as _importlib

try:
    from importlib.metadata import version  # for Python 3.8+
except ImportError:
    from pkg_resources import get_distribution, DistributionNotFound
    try:
        __version__ = get_distribution(__name__).version
    except DistributionNotFound:
        # Package is not installed
        __version__ = 'unknown'
else:
    __version__ = version(__name__)



submodules = [
    'components',
    'slides',
]

__all__ = submodules + [
    'test',
]


def __dir__():
    return __all__


def __getattr__(name):
    if name in submodules:
        return _importlib.import_module(f'bymanim.{name}')
    else:
        try:
            return globals()[name]
        except KeyError:
            raise AttributeError(
                f"Module 'bymanim' has no attribute '{name}'"
            )