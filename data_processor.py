
from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self):
        self._data: list[str] = []
        self._rank = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self._data:
            raise IndexError("No data available")

        value = self._data.pop(0)
        rank = self._rank
        self._rank += 1

        return rank, value


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if type(data) in (int, float):
            return True

        if isinstance(data, list):
            return all(type(item) in (int, float) for item in data)

        return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise TypeError("Improper numeric data")

        if not isinstance(data, list):
            data = [data]

        for item in data:
            self._data.append(str(item))


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True

        if isinstance(data, list):
            return all(isinstance(item, str) for item in data)

        return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise TypeError("Improper text data")

        if not isinstance(data, list):
            data = [data]

        for item in data:
            self._data.append(item)


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            return all(
                isinstance(key, str) and isinstance(value, str)
                for key, value in data.items()
            )

        if isinstance(data, list):
            return all(
                isinstance(item, dict)
                and all(
                    isinstance(key, str) and isinstance(value, str)
                    for key, value in item.items()
                )
                for item in data
            )

        return False

    def ingest(
        self, data: dict[str, str] | list[dict[str, str]]
    ) -> None:
        if not self.validate(data):
            raise TypeError("Improper log data")

        if not isinstance(data, list):
            data = [data]

        for item in data:
            if "log_level" in item and "log_message" in item:
                value = item["log_level"] + ": " + item["log_message"]
            else:
                value = str(item)

            self._data.append(value)


if __name__ == "__main__":
    print("=== Code Nexus - Data Processor ===")

    print("\nTesting Numeric Processor...")
    numeric = NumericProcessor()

    print(f"Trying to validate input '42': {numeric.validate(42)}")
    print(f"Trying to validate input 'Hello': {numeric.validate('Hello')}")

    print("Test invalid ingestion of string 'foo' without prior validation:")
    try:
        numeric.ingest("foo")
    except TypeError as error:
        print(f"Got exception: {error}")

    numbers = [1, 2, 3, 4, 5]
    print(f"Processing data: {numbers}")
    numeric.ingest(numbers)

    print("Extracting 3 values...")
    for _ in range(3):
        rank, value = numeric.output()
        print(f"Numeric value {rank}: {value}")

    print("\nTesting Text Processor...")
    text = TextProcessor()

    print(f"Trying to validate input '42': {text.validate(42)}")

    words = ["Hello", "Nexus", "World"]
    print(f"Processing data: {words}")
    text.ingest(words)

    print("Extracting 1 value...")
    rank, value = text.output()
    print(f"Text value {rank}: {value}")

    print("\nTesting Log Processor...")
    logs = LogProcessor()

    print(f"Trying to validate input 'Hello': {logs.validate('Hello')}")

    entries = [
        {"log_level": "NOTICE", "log_message": "Connection to server"},
        {"log_level": "ERROR", "log_message": "Unauthorized access!!"}
    ]

    print(f"Processing data: {entries}")
    logs.ingest(entries)

    print("Extracting 2 values...")
    for _ in range(2):
        rank, value = logs.output()
        print(f"Log entry {rank}: {value}")
