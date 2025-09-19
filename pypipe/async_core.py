# pypipe/async_core.py

from abc import ABC, abstractmethod
from typing import Any, AsyncIterable, Callable, List


class AsyncDataSource(ABC):
    """Abstract base class for async data sources."""

    @abstractmethod
    async def read(self) -> AsyncIterable[Any]:
        pass


class AsyncTransformation(ABC):
    """Abstract base class for async data transformations."""

    @abstractmethod
    def process(self, data: AsyncIterable[Any]) -> AsyncIterable[Any]:
        pass


class AsyncFunctionalTransformation(AsyncTransformation):
    """An async transformation that applies an async function to the data."""

    def __init__(self, process_func: Callable[[AsyncIterable[Any]], AsyncIterable[Any]]) -> None:
        self._process_func = process_func

    def process(self, data: AsyncIterable[Any]) -> AsyncIterable[Any]:
        return self._process_func(data)


def async_transformation(
    func: Callable[[AsyncIterable[Any]], AsyncIterable[Any]],
) -> AsyncFunctionalTransformation:
    """Decorator to turn a function into an AsyncTransformation."""
    return AsyncFunctionalTransformation(func)


class AsyncDataSink(ABC):
    """Abstract base class for async data sinks."""

    @abstractmethod
    async def write(self, data: AsyncIterable[Any]) -> None:
        pass


class AsyncPipeline:
    """An asynchronous declarative pipeline to chain data processing steps."""

    def __init__(self, source: AsyncDataSource) -> None:
        self._source = source
        self._steps: List[AsyncTransformation | AsyncDataSink] = []

    def add(
        self, transformation: AsyncTransformation, index: int | None = None
    ) -> "AsyncPipeline":
        if index is None:
            self._steps.append(transformation)
        else:
            self._steps.insert(index, transformation)
        return self

    def to(self, sink: AsyncDataSink) -> "AsyncPipeline":
        self._steps.append(sink)
        return self

    async def run(self) -> None:
        if not any(isinstance(step, AsyncDataSink) for step in self._steps):
            raise ValueError("At least one data sink must be set for the pipeline.")

        data_stream = self._source.read()

        for i, step in enumerate(self._steps):
            if isinstance(step, AsyncTransformation):
                data_stream = step.process(data_stream)
            elif isinstance(step, AsyncDataSink):
                is_last_step = i == len(self._steps) - 1
                if not is_last_step:
                    items = [item async for item in data_stream]
                    await step.write(self._list_to_async_iterable(items))
                    data_stream = self._list_to_async_iterable(items)
                else:
                    await step.write(data_stream)

    async def _list_to_async_iterable(self, items: List[Any]) -> AsyncIterable[Any]:
        for item in items:
            yield item


# --- Default Async Components ---


class AsyncListSource(AsyncDataSource):
    """A simple async data source that reads from a Python list."""

    def __init__(self, data: List[Any]) -> None:
        self._data = data

    async def read(self) -> AsyncIterable[Any]:
        for item in self._data:
            yield item


class AsyncConsoleSink(AsyncDataSink):
    """A simple async data sink that prints each item to the console."""

    async def write(self, data: AsyncIterable[Any]) -> None:
        async for item in data:
            print(item)
