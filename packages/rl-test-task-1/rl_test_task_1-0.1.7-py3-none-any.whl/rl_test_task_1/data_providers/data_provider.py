from abc import ABC, abstractmethod
from typing import Any


class DataProvider(ABC):
    @abstractmethod
    def get(self) -> Any:
        pass
