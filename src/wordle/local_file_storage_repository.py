from typing import Any
import yaml
import os

from wordle.i_repository import IRepository


class LocalFileStorageRepository(IRepository):
    def __init__(self, *args, **kwargs):
        # TODO error handling or default
        self._datastore_path = os.getenv("DATASTORE_PATH")
        super().__init__(*args, **kwargs)
        try:
            with open(self._datastore_path, "x") as f:
                yaml.dump({}, f, Dumper=yaml.Dumper, indent=2)
        except FileExistsError:
            pass

    def get(self, key: str) -> Any:
        with open(self._datastore_path, "r") as f:
            data = yaml.load(f, Loader=yaml.Loader) or {}
            return data.get(key)

    def save(self, key: str, value: Any) -> Any:
        data = None
        with open(self._datastore_path, "r") as f:
            data = yaml.load(f, Loader=yaml.Loader) or {}
        with open(self._datastore_path, "w") as f:
            data[key] = value
            yaml.dump(data, f, Dumper=yaml.Dumper, indent=2)
