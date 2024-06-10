import logging

from ..models.input import Input


class InputDataParser:
    __logger: logging.Logger = logging.getLogger(__name__)

    def parse(self, input: Input) -> dict[int, str]:
        parsed_data: dict[int, str] = {}

        lines: list[str] = input.data.split('\n')

        for line in lines:
            key_value: tuple[int,
                             str] | None = self.__get_key_value_pairs(line)

            if key_value is None:
                continue

            key, value = key_value
            parsed_data[key] = value

        return parsed_data

    def __get_key_value_pairs(self, line: str) -> tuple[int, str] | None:
        parts: list[str] = line.strip().split()
        return self.__disassemble_parts(parts)

    def __disassemble_parts(self, parts: list[str]) -> tuple[int, str] | None:
        try:
            key: int = int(parts[1])
            value: str = parts[0]

            return (key, value)

        except IndexError:
            self.__logger.error('Index out of range.')

        return None
