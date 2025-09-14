
"""
PyPipe: A declarative data processing framework.
"""

from .core import (
    DataSource,
    Transformation,
    DataSink,
    Pipeline,
    ListSource,
    ConsoleSink,
)

__all__ = [
    "DataSource",
    "Transformation",
    "DataSink",
    "Pipeline",
    "ListSource",
    "ConsoleSink",
]
