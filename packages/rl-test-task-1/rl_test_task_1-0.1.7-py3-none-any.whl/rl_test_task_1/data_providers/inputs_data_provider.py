import os
import sys
from typing import Sequence

from dotenv import load_dotenv
from rl_test_common import Config
from rl_test_storage_handlers.params.storage_data import StorageData
from rl_test_storage_handlers.params.storage_destination import \
    StorageDestination
from rl_test_storage_handlers.storage_handler import StorageHandler

from .data_provider import DataProvider
from .exceptions.too_big_input_data import TooBigInputData
from .models.input import Input

load_dotenv()


class InputsDataProvider(DataProvider):
    __config: Config = Config(os.getenv('CONFIG_FILE_PATH'))

    __input_data_size_in_bytes: int = 0

    __inputs: list[Input] = []

    def __init__(self, storage_handler: StorageHandler,
                 destinations: Sequence[StorageDestination]) -> None:
        for destination in destinations:
            data: StorageData = storage_handler.read(destination)

            self.__input_data_size_in_bytes += sys.getsizeof(data.get())
            self.__check_input_data_size()

            self.__inputs.append(Input(data.get()))

    def __check_input_data_size(self) -> None:
        if self.__input_data_size_in_bytes > self.__config.task_1_max_input_data_size_in_bytes:
            raise TooBigInputData(
                self.__input_data_size_in_bytes,
                self.__config.task_1_max_input_data_size_in_bytes)

    def get(self) -> list[Input]:
        return self.__inputs
