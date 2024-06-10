from rl_test_common import Common
from rl_test_storage_handlers.file.params.file_data import FileData
from rl_test_storage_handlers.file.params.file_destination import \
    FileDestination
from rl_test_storage_handlers.params.storage_destination import \
    StorageDestination
from rl_test_storage_handlers.storage_handler import StorageHandler

from ..data_providers.models.person import Person
from ..data_providers.parsers.output_data_parser import OutputDataParser
from ..data_providers.persons_data_provider import PersonsDataProvider
from .exceptions.unsupported_data_type import UnsupportedDataType
from .generic_data_exporter import GenericDataExporter


class PersonsDataExporter(GenericDataExporter):
    __common: Common = Common()

    __output_data_parser: OutputDataParser = OutputDataParser()

    def __init__(self, storage_handler: StorageHandler, data_provider: PersonsDataProvider) -> None:
        super().__init__(storage_handler, data_provider)

    def export(self, destination: StorageDestination) -> None:
        persons: list[Person] = super()._data_provider.get()
        self.__export(destination, persons)

    def export_sorted(self, destination: StorageDestination) -> None:
        persons: list[Person] = super()._data_provider.get()
        persons_sorted: list[Person] = sorted(
            persons, key=lambda person: person.id)
        self.__export(destination, persons_sorted)

    def __export(self, destination: StorageDestination, persons: list[Person]) -> None:
        destination_type: str = self.__common.get_type(destination)

        if destination_type is FileDestination.__name__:
            data: FileData = FileData(self.__output_data_parser.parse(persons))
            super()._export(destination, data)

        else:
            raise UnsupportedDataType(destination_type)
