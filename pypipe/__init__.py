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
from .async_core import (
    AsyncDataSource,
    AsyncTransformation,
    AsyncFunctionalTransformation,
    async_transformation,
    AsyncDataSink,
    AsyncPipeline,
    AsyncListSource,
    AsyncConsoleSink,
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
