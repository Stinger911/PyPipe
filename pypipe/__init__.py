"""
PyPipe: A declarative data processing framework.
"""

from .async_core import (
    AsyncConsoleSink,
    AsyncDataSink,
    AsyncDataSource,
    AsyncFunctionalTransformation,
    AsyncListSource,
    AsyncPipeline,
    AsyncTransformation,
    async_transformation,
)
from .core import (
    ConsoleSink,
    DataSink,
    DataSource,
    FileSink,
    FunctionalTransformation,
    ListSource,
    Pipeline,
    Transformation,
    transformation,
)

__all__ = [
    # Sync
    "DataSource",
    "Transformation",
    "FunctionalTransformation",
    "transformation",
    "DataSink",
    "Pipeline",
    "ListSource",
    "ConsoleSink",
    "FileSink",
    # Async
    "AsyncDataSource",
    "AsyncTransformation",
    "AsyncFunctionalTransformation",
    "async_transformation",
    "AsyncDataSink",
    "AsyncPipeline",
    "AsyncListSource",
    "AsyncConsoleSink",
]
