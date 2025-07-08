# -*- coding: utf-8 -*-

"""Sphinx plugin to create treemaps based on Cobertura data."""

from .treemap import setup

try:
    from ._version import __version__
except ImportError:
    __version__ = "unknown"

__all__ = ['setup', '__version__']
