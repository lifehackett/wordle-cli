from dataclasses import dataclass
import os
import yaml

from typing import TypeVar

Self = TypeVar("Self", bound="WordleResults")


@dataclass
class Result:
    answer: str
    guesses: list[str]


class WordleResults():
    def __init__(self, results: dict[str, Result]):
        self.results = results

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


class WordleResultsYAMLMarshaller:
    @classmethod
    def load(self, file_path: str) -> WordleResults:
        try:
            with open(file_path, "r") as f:
                results = yaml.load(f, Loader=yaml.Loader) or {}
                results = {key: Result(
                    answer=value["answer"], guesses=value["guesses"]) for key, value in results.items()}
                return WordleResults(results)

        except FileNotFoundError as e:
            raise FileNotFoundError(
                "Results file not found. Provide a valid envvar RESULTS_PATH"
            )

    @classmethod
    def dump(self, file_path: str, results: WordleResults):
        try:
            with open(file_path, "w") as f:
                out_results = {}
                for key, value in results.results.items():
                    out_results[key] = {
                        "answer": value.answer,
                        "guesses": value.guesses
                    }
                yaml.dump(out_results, f, Dumper=yaml.Dumper, indent=2)
        except FileNotFoundError as e:
            raise FileNotFoundError(
                "Results file not found. Provide a valid envvar RESULTS_PATH"
            )
