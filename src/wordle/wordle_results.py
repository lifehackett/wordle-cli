from dataclasses import dataclass
import os
import yaml

from typing import TypeVar

Self = TypeVar("Self", bound="WordleResults")


@dataclass
class Result:
    answer: str
    guesses: list[str]


class WordleResults(yaml.YAMLObject):
    results_path = os.getenv("RESULTS_PATH", "")
    yaml_tag = "!WordleResults"

    def __init__(self, results: dict[str, Result]):
        self.results = results

    def __repr__(self):
        return f"{self.__class__.__name__}(results={self.results})"

    @classmethod
    def load(cls) -> Self:
        try:
            with open(cls.results_path, "r") as f:
                return yaml.load(f, Loader=yaml.Loader)
        except FileNotFoundError as e:
            raise FileNotFoundError(
                "Results file not found. Provide a valid envvar RESULTS_PATH"
            )

    def save(self):
        try:
            with open(WordleResults.results_path, "w") as f:
                yaml.dump(self, f, Dumper=yaml.Dumper, indent=2)
        except FileNotFoundError as e:
            raise FileNotFoundError(
                "Results file not found. Provide a valid envvar RESULTS_PATH"
            )

    def create_result(self, date_key: str, answer: str):
        self.results.setdefault(date_key, Result(answer, []))

    def get_result(self, date_key: str) -> Result:
        return self.results.get(date_key)

    def add_guess(self, date_key, guess):
        if date_key not in self.results:
            raise IndexError(
                f"No result found for date_key: {date_key}. Call create_result first."
            )
        self.results[date_key].guesses.append(guess)
