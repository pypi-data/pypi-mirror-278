from rl_test_storage_handlers.params.storage_data import StorageData
from rl_test_storage_handlers.params.storage_destination import \
    StorageDestination
from rl_test_storage_handlers.storage_handler import StorageHandler

from ..data_providers.data_provider import DataProvider
from .data_exporter import DataExporter


class GenericDataExporter(DataExporter):
    def __init__(self, storage_handler: StorageHandler, data_provider: DataProvider) -> None:
        super().__init__(storage_handler, data_provider)

    def _export(self, destination: StorageDestination, data: StorageData) -> None:
        super()._storage_handler.write(destination, data)
