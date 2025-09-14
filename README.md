# pypipe

A simple and declarative data processing pipeline for Python.

## Installation

This project uses Poetry for dependency management. To install the dependencies, run:

```bash
poetry install
```

## Core Concepts

The pipeline is built around three core components:

*   **`DataSource`**: Reads data from a source (e.g., a list, a file).
*   **`Transformation`**: Processes the data. A pipeline can have multiple transformations chained together.
*   **`DataSink`**: Writes the data to a destination (e.g., the console, a file).

## Getting Started

Here's a simple example of how to use `pypipe`:

```python
from pypipe.core import Pipeline, ListSource, ConsoleSink, Transformation

# 1. Define a custom transformation
class Uppercase(Transformation):
    def process(self, data):
        return (item.upper() for item in data)

# 2. Create a pipeline
pipeline = Pipeline(ListSource(["hello", "world"]))
pipeline.add(Uppercase())
pipeline.to(ConsoleSink())

# 3. Run the pipeline
pipeline.run()
```

This will output:
```
HELLO
WORLD
```

## Advanced Usage

### Multiple Sinks

You can add multiple sinks at any point in the pipeline.

```python
from pypipe.core import FileSink

pipeline = Pipeline(ListSource(["hello", "world"]))
pipeline.add(Uppercase())
pipeline.to(ConsoleSink()) # First sink
pipeline.add(Exclaim())
pipeline.to(FileSink("output.txt")) # Second sink
```

### One-to-Many Transformations

Transformations can change the number of items in the pipeline. For example, splitting sentences into words:

```python
class Splitter(Transformation):
    def process(self, data):
        for sentence in data:
            for word in sentence.split():
                yield word

pipeline = Pipeline(ListSource(["hello world", "foo bar"]))
pipeline.add(Splitter())
pipeline.to(ConsoleSink())
pipeline.run()
```

This will output:
```
hello
world
foo
bar
```

### Functional Transformations

For simple transformations, you can use `FunctionalTransformation` with a lambda function, avoiding the need to create a new class for each transformation.

```python
from pypipe.core import FunctionalTransformation

pipeline = Pipeline(ListSource(["hello", "world"]))
pipeline.add(FunctionalTransformation(lambda data: (item.upper() for item in data)))
pipeline.to(ConsoleSink())
pipeline.run()
```

### Transformation Decorator

For even more convenience, you can use the `@transformation` decorator to turn a function into a `Transformation` instance.

```python
from pypipe.core import transformation

@transformation
def uppercase(data):
    return (item.upper() for item in data)

pipeline = Pipeline(ListSource(["hello", "world"]))
pipeline.add(uppercase)
pipeline.to(ConsoleSink())
pipeline.run()
```

### Adding Transformations at Arbitrary Positions

You can insert a transformation at a specific index in the pipeline.

```python
pipeline = Pipeline(ListSource(["a", "b", "c"]))
pipeline.add(Uppercase())
pipeline.add(Exclaim())
pipeline.to(ConsoleSink())

# Insert a reverse transformation at index 1
pipeline.add(FunctionalTransformation(lambda data: reversed(list(data))), index=1)

pipeline.run()
```
This will output:
```
C!
B!
A!
```

## Running Tests

To run the tests, execute the following command from the root directory:

```bash
python -m unittest discover tests
```
