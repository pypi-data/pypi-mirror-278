from abc import ABC, abstractmethod

from rl_test_common import Common
from rl_test_storage_handlers.params.storage_destination import \
    StorageDestination
from rl_test_storage_handlers.storage_handler import StorageHandler

from ..data_providers.data_provider import DataProvider


class DataExporter(ABC):
    __common: Common = Common()

    __storage_handler: StorageHandler | None = None

    __data_provider: DataProvider | None = None

    def __init__(self, storage_handler: StorageHandler, data_provider: DataProvider) -> None:
        self.__storage_handler = storage_handler
        self.__data_provider = data_provider

    @property
    def _storage_handler(self) -> StorageHandler:
        if self.__storage_handler is None:
            type: str = self.__common.get_type(self.__storage_handler)
            raise AttributeError(f'{type} object is None.')

        return self.__storage_handler

    @property
    def _data_provider(self) -> DataProvider:
        if self.__data_provider is None:
            type: str = self.__common.get_type(self.__data_provider)
            raise AttributeError(f'{type} object is None.')

        return self.__data_provider

    @abstractmethod
    def export(self, destination: StorageDestination) -> None:
        pass
