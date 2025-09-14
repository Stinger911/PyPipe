from abc import ABC, abstractmethod
from typing import Any, Callable, Iterable, List

# --- Framework Core ---

class DataSource(ABC):
    """Abstract base class for data sources."""
    @abstractmethod
    def read(self) -> Iterable[Any]:
        """Read data from the source and return an iterable."""
        pass

class Transformation(ABC):
    """Abstract base class for data transformations."""
    @abstractmethod
    def process(self, data: Iterable[Any]) -> Iterable[Any]:
        """Process the data and return an iterable of the transformed data."""
        pass

class FunctionalTransformation(Transformation):
    """A transformation that applies a function to the data."""
    def __init__(self, process_func: Callable[[Iterable[Any]], Iterable[Any]]):
        self._process_func = process_func

    def process(self, data: Iterable[Any]) -> Iterable[Any]:
        return self._process_func(data)

class DataSink(ABC):
    """Abstract base class for data sinks."""
    @abstractmethod
    def write(self, data: Iterable[Any]) -> None:
        """Write the data to the sink."""
        pass

class Pipeline:
    """
    A declarative pipeline to chain data processing steps.
    """
    def __init__(self, source: DataSource):
        self._source = source
        self._steps: List[Transformation | DataSink] = []

    def add(self, transformation: Transformation, index: int | None = None) -> "Pipeline":
        """
        Adds a transformation step to the pipeline.
        By default, it's added to the end.
        """
        if index is None:
            self._steps.append(transformation)
        else:
            self._steps.insert(index, transformation)
        return self

    def to(self, sink: DataSink) -> "Pipeline":
        """Adds a data sink to the pipeline."""
        self._steps.append(sink)
        return self

    def run(self) -> None:
        """Executes the entire data processing pipeline."""
        if not any(isinstance(step, DataSink) for step in self._steps):
            raise ValueError("At least one data sink must be set for the pipeline using .to()")

        # Read from the source
        data = self._source.read()

        # Apply all steps in sequence
        for i, step in enumerate(self._steps):
            if isinstance(step, Transformation):
                data = step.process(data)
            elif isinstance(step, DataSink):
                # If the sink is not the last step, we need to make sure the data is not a consumed generator.
                is_last_step = (i == len(self._steps) - 1)
                if not is_last_step:
                    # materialize the generator if it is one
                    data_list = list(data)
                    step.write(data_list)
                    data = data_list
                else:
                    step.write(data)

# --- Default Components ---

class ListSource(DataSource):
    """A simple data source that reads from a Python list."""
    def __init__(self, data: List[Any]):
        self._data = data

    def read(self) -> Iterable[Any]:
        return self._data

class ConsoleSink(DataSink):
    """A simple data sink that prints each item to the console."""
    def write(self, data: Iterable[Any]) -> None:
        for item in data:
            print(item)

class FileSink(DataSink):
    """A simple data sink that writes each item to a file."""
    def __init__(self, filename: str):
        self._filename = filename

    def write(self, data: Iterable[Any]) -> None:
        with open(self._filename, 'w') as f:
            for item in data:
                f.write(str(item) + '\n')