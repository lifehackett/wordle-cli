import pytest
import os

from wordle.i_repository import IRepository
from wordle.local_file_storage_repository import LocalFileStorageRepository


@pytest.fixture
def repository():
    return LocalFileStorageRepository()


def test_missing_datastore_file():
    os.remove("./tests/wordle/datastore.yaml")
    repository = LocalFileStorageRepository()
    repository.get("foo")


class TestGet:
    def test_missing_key_success(self, repository: LocalFileStorageRepository):
        value = repository.get("unknown_key")
        assert value is None


class TestSave:
    def test_new_key_success(self, repository: LocalFileStorageRepository):
        repository.save("test_key", "test_value")
        value = repository.get("test_key")
        assert value == "test_value"

    def test_existing_key_success(self, repository: LocalFileStorageRepository):
        repository.save("test_key", "test_value")
        repository.save("test_key", "updated_test_value")
        value = repository.get("test_key")
        assert value == "updated_test_value"

    def test_save_dict_success(self, repository: LocalFileStorageRepository):
        repository.save("test_key", {"foo": "bar"})
        value = repository.get("test_key")
        assert value == {"foo": "bar"}

    def test_save_list_success(self, repository: LocalFileStorageRepository):
        repository.save("test_key", ["foo", "bar"])
        value = repository.get("test_key")
        assert value == ["foo", "bar"]
