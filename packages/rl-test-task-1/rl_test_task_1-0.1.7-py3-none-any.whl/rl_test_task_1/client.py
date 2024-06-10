import os

from dotenv import load_dotenv
from rl_test_common import Config
from rl_test_storage_handlers.file.params.file_destination import \
    FileDestination
from rl_test_storage_handlers.file.text_file_handler import TextFileHandler

from .data_exporters.persons_data_exporter import PersonsDataExporter
from .data_providers.inputs_data_provider import InputsDataProvider
from .data_providers.persons_data_provider import PersonsDataProvider

load_dotenv()


class Client:
    __config: Config = Config(os.getenv('CONFIG_FILE_PATH'))

    __text_file_handler: TextFileHandler = TextFileHandler()

    def client_code(self) -> None:
        inputs_data_provider: InputsDataProvider = self.__get_inputs_data_provider()

        persons_data_provider: PersonsDataProvider = PersonsDataProvider(
            inputs_data_provider)

        persons_data_exporter: PersonsDataExporter = PersonsDataExporter(
            self.__text_file_handler, persons_data_provider)

        output_file_destination: FileDestination = FileDestination(
            self.__config.task_1_output_file_name)

        persons_data_exporter.export_sorted(output_file_destination)

    def __get_inputs_data_provider(self) -> InputsDataProvider:
        return InputsDataProvider(
            self.__text_file_handler,
            self.__get_input_file_destinations())

    def __get_input_file_destinations(self) -> list[FileDestination]:
        file_names: list[str] = [
            self.__config.task_1_first_input_file_name,
            self.__config.task_1_second_input_file_name
        ]

        return [FileDestination(file_name) for file_name in file_names]
