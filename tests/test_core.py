import unittest
from pypipe.core import Pipeline, DataSource, DataSink, Transformation
from typing import Any, Iterable, List

# Mock components for testing
class MockDataSource(DataSource):
    def __init__(self, data: List[Any]):
        self._data = data
    def read(self) -> Iterable[Any]:
        return self._data

class MockTransformation(Transformation):
    def __init__(self, transformation_func):
        self.transformation_func = transformation_func
    def process(self, data: Iterable[Any]) -> Iterable[Any]:
        return self.transformation_func(data)

class MockDataSink(DataSink):
    def __init__(self):
        self.data = []
    def write(self, data: Iterable[Any]) -> None:
        self.data.extend(list(data))

class TestPipeline(unittest.TestCase):

    def test_multiple_sinks(self):
        # 1. Prepare the initial dataset and mock components
        initial_data = ["a", "b", "c"]
        source = MockDataSource(initial_data)
        
        uppercase = MockTransformation(lambda data: [item.upper() for item in data])
        exclaim = MockTransformation(lambda data: [f"{item}!" for item in data])
        
        sink1 = MockDataSink()
        sink2 = MockDataSink()

        # 2. Build the pipeline with multiple sinks
        pipeline = Pipeline(source)
        pipeline.add(uppercase).to(sink1).add(exclaim).to(sink2)

        # 3. Run the pipeline
        pipeline.run()

        # 4. Assert the results
        self.assertEqual(sink1.data, ["A", "B", "C"])
        self.assertEqual(sink2.data, ["A!", "B!", "C!"])

    def test_generator_consumption(self):
        # Test that generators are not exhausted by intermediate sinks
        initial_data = ["a", "b", "c"]
        source = MockDataSource(initial_data)

        # This transformation returns a generator
        uppercase_generator = MockTransformation(lambda data: (item.upper() for item in data))
        exclaim = MockTransformation(lambda data: [f"{item}!" for item in data])

        sink1 = MockDataSink()
        sink2 = MockDataSink()

        pipeline = Pipeline(source)
        pipeline.add(uppercase_generator).to(sink1).add(exclaim).to(sink2)

        pipeline.run()

        self.assertEqual(sink1.data, ["A", "B", "C"])
        self.assertEqual(sink2.data, ["A!", "B!", "C!"])

    def test_one_to_many_transformation(self):
        # Test a transformation that increases the number of items
        initial_data = ["hello world", "foo bar"]
        source = MockDataSource(initial_data)

        def split_into_words(data):
            for sentence in data:
                for word in sentence.split():
                    yield word
        
        splitter = MockTransformation(split_into_words)
        
        sink = MockDataSink()

        pipeline = Pipeline(source)
        pipeline.add(splitter).to(sink)

        pipeline.run()

        self.assertEqual(sink.data, ["hello", "world", "foo", "bar"])

    def test_add_at_index(self):
        initial_data = ["a", "b", "c"]
        source = MockDataSource(initial_data)

        uppercase = MockTransformation(lambda data: [item.upper() for item in data])
        exclaim = MockTransformation(lambda data: [f"{item}!" for item in data])
        reverse = MockTransformation(lambda data: list(reversed(list(data))))

        sink = MockDataSink()

        pipeline = Pipeline(source)
        pipeline.add(uppercase).add(exclaim).to(sink)

        # Insert the reverse transformation at index 1 (after uppercase)
        pipeline.add(reverse, index=1)

        pipeline.run()

        # The order should be: uppercase -> reverse -> exclaim
        self.assertEqual(sink.data, ["C!", "B!", "A!"])


if __name__ == '__main__':
    unittest.main()