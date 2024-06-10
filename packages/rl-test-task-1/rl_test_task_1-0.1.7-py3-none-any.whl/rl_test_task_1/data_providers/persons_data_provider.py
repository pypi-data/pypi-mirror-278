from .data_provider import DataProvider
from .inputs_data_provider import InputsDataProvider
from .models.input import Input
from .models.person import Person
from .parsers.input_data_parser import InputDataParser


class PersonsDataProvider(DataProvider):
    __input_data_parser: InputDataParser = InputDataParser()

    __inputs_data_provider: InputsDataProvider | None = None

    def __init__(self, inputs_data_provider: InputsDataProvider) -> None:
        self.__inputs_data_provider = inputs_data_provider

    def get(self) -> list[Person]:
        first_names: dict[int, str] = self.__get_first_names()
        last_names: dict[int, str] = self.__get_last_names()

        return self.__merge(first_names, last_names)

    def __get_first_names(self) -> dict[int, str]:
        first_names: dict[int, str] = {}

        if self.__inputs_data_provider is not None:
            input: Input = self.__inputs_data_provider.get()[0]
            first_names = self.__input_data_parser.parse(input)

        return first_names

    def __get_last_names(self) -> dict[int, str]:
        last_names: dict[int, str] = {}

        if self.__inputs_data_provider is not None:
            input: Input = self.__inputs_data_provider.get()[1]
            last_names = self.__input_data_parser.parse(input)

        return last_names

    def __merge(self, first_names: dict[int, str], last_names: dict[int, str]) -> list[Person]:
        persons: list[Person] = []

        for id in first_names:
            if id in last_names:
                first_name: str = first_names[id]
                last_name: str = last_names[id]

                persons.append(Person(id, first_name, last_name))

        return persons
