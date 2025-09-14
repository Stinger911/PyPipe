from pypipe.core import ConsoleSink, ListSource, Pipeline, Transformation, FileSink
from typing import Any, Iterable


def main():
    """Defines and runs the example data processing pipeline."""

    # --- Example 1: Simple Uppercase and Exclaim ---

    class Uppercase(Transformation):
        """A simple transformation that converts string data to uppercase."""
        def process(self, data: Iterable[str]) -> Iterable[str]:
            print("  - Applying Uppercase transformation...")
            return (item.upper() for item in data)

    class Exclaim(Transformation):
        """A simple transformation that appends an exclamation mark to string data."""
        def process(self, data: Iterable[str]) -> Iterable[str]:
            print("  - Applying Exclaim transformation...")
            return (f"{item}!" for item in data)

    sample_data = ["hello", "world", "this is a", "declarative pipeline"]
    print(f"Initial data: {sample_data}")

    pipeline1 = Pipeline(ListSource(sample_data))
    pipeline1.add(Uppercase()).to(ConsoleSink()).add(Exclaim()).to(FileSink("output.txt"))

    print("\nRunning pipeline 1...")
    pipeline1.run()
    print("\nPipeline 1 finished.")

    # --- Example 2: Splitting strings and processing tokens ---

    class Splitter(Transformation):
        """Splits sentences into words."""
        def process(self, data: Iterable[str]) -> Iterable[str]:
            print("  - Applying Splitter transformation...")
            for sentence in data:
                for word in sentence.split():
                    yield word
    
    class Capitalize(Transformation):
        """Capitalizes each word."""
        def process(self, data: Iterable[str]) -> Iterable[str]:
            print("  - Applying Capitalize transformation...")
            return (word.capitalize() for word in data)

    sentence_data = ["this is a sentence", "and this is another one"]
    print(f"\nInitial sentence data: {sentence_data}")

    pipeline2 = Pipeline(ListSource(sentence_data))
    pipeline2.add(Splitter()).add(Capitalize()).to(ConsoleSink())

    print("\nRunning pipeline 2...")
    pipeline2.run()
    print("\nPipeline 2 finished.")


if __name__ == "__main__":
    main()
