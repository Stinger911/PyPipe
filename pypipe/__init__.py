"""
PyPipe: A declarative data processing framework.
"""

from .core import (
    DataSource,
    Transformation,
    FunctionalTransformation,
    transformation,
    DataSink,
    Pipeline,
    ListSource,
    ConsoleSink,
    FileSink,
)

__all__ = [
    "DataSource",
    "Transformation",
    "FunctionalTransformation",
    "transformation",
    "DataSink",
    "Pipeline",
    "ListSource",
    "ConsoleSink",
    "FileSink",
]