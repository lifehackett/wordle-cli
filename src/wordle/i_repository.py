from abc import ABC, abstractmethod


class IRepository(ABC):
    @abstractmethod
    def get(self, key: str) -> str:
        pass

    @abstractmethod
    def save(self, key: str, value: str) -> str:
        pass
