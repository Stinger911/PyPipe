import asyncio
import unittest
from typing import Any, AsyncIterable, List

from pypipe.async_core import (
    AsyncDataSink,
    AsyncDataSource,
    AsyncFunctionalTransformation,
    AsyncPipeline,
    async_transformation,
)


# Mock components for testing
class MockAsyncDataSource(AsyncDataSource):
    def __init__(self, data: List[Any]):
        self._data = data

    async def read(self) -> AsyncIterable[Any]:
        for item in self._data:
            yield item


class MockAsyncDataSink(AsyncDataSink):
    def __init__(self):
        self.data = []

    async def write(self, data: AsyncIterable[Any]) -> None:
        async for item in data:
            self.data.append(item)


class TestAsyncPipeline(unittest.IsolatedAsyncioTestCase):
    async def test_simple_pipeline(self):
        source = MockAsyncDataSource([1, 2, 3])
        sink = MockAsyncDataSink()

        @async_transformation
        async def add_one(data):
            async for item in data:
                yield item + 1

        pipeline = AsyncPipeline(source)
        pipeline.add(add_one).to(sink)

        await pipeline.run()

        self.assertEqual(sink.data, [2, 3, 4])

    async def test_multiple_sinks(self):
        source = MockAsyncDataSource(["a", "b", "c"])
        sink1 = MockAsyncDataSink()
        sink2 = MockAsyncDataSink()

        @async_transformation
        async def uppercase(data):
            async for item in data:
                yield item.upper()

        @async_transformation
        async def exclaim(data):
            async for item in data:
                yield f"{item}!"

        pipeline = AsyncPipeline(source)
        pipeline.add(uppercase).to(sink1).add(exclaim).to(sink2)

        await pipeline.run()

        self.assertEqual(sink1.data, ["A", "B", "C"])
        self.assertEqual(sink2.data, ["A!", "B!", "C!"])

    async def test_one_to_many_transformation(self):
        source = MockAsyncDataSource(["hello world", "foo bar"])
        sink = MockAsyncDataSink()

        @async_transformation
        async def splitter(data):
            async for sentence in data:
                for word in sentence.split():
                    yield word

        pipeline = AsyncPipeline(source)
        pipeline.add(splitter).to(sink)

        await pipeline.run()

        self.assertEqual(sink.data, ["hello", "world", "foo", "bar"])

    async def test_functional_transformation(self):
        source = MockAsyncDataSource(["a", "b", "c"])
        sink = MockAsyncDataSink()

        async def uppercase_func(data):
            async for item in data:
                yield item.upper()

        uppercase = AsyncFunctionalTransformation(uppercase_func)

        pipeline = AsyncPipeline(source)
        pipeline.add(uppercase).to(sink)

        await pipeline.run()

        self.assertEqual(sink.data, ["A", "B", "C"])

    async def test_async_transformation(self):
        source = MockAsyncDataSource([1, 2, 3])
        sink = MockAsyncDataSink()
        executed = []

        @async_transformation
        async def async_increment(data):
            async for item in data:
                print(f"[inc] Processing {item} asynchronously")
                executed.append(f"inc:{item}")
                await asyncio.sleep(1)  # Simulate async work
                yield item + 1

        @async_transformation
        async def async_to_str(data):
            async for item in data:
                print(f"[str] Converting {item} to string asynchronously")
                executed.append(f"str:{item}")
                await asyncio.sleep(0.5)  # Simulate async work
                yield str(item)

        pipeline = AsyncPipeline(source)
        pipeline.add(async_increment).add(async_to_str).to(sink)

        await pipeline.run()

        self.assertEqual(sink.data, ["2", "3", "4"])
        self.assertEqual(
            executed, ["inc:1", "str:2", "inc:2", "str:3", "inc:3", "str:4"]
        )


if __name__ == "__main__":
    unittest.main()
