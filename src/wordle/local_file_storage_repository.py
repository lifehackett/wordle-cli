from typing import Any
import yaml

from wordle.i_repository import IRepository


class LocalFileStorageRepository(IRepository):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            with open(self._datastore_filename, "x") as f:
                yaml.dump({}, f, Dumper=yaml.Dumper, indent=2)
        except FileExistsError:
            pass

    @property
    def _datastore_filename(self):
        return "./tests/wordle/datastore.yaml"

    def get(self, key: str) -> Any:
        with open(self._datastore_filename, "r") as f:
            data = yaml.load(f, Loader=yaml.Loader)
            return data.get(key)

    def save(self, key: str, value: Any) -> Any:
        with open(self._datastore_filename, "w+") as f:
            data = yaml.load(f, Loader=yaml.Loader) or {}
            data.setdefault(key, value)
            yaml.dump(data, f, Dumper=yaml.Dumper, indent=2)
