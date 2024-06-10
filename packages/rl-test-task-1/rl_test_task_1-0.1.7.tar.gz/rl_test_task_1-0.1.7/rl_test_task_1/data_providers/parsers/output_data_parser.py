from ..models.person import Person


class OutputDataParser:
    def parse(self, persons: list[Person]) -> str:
        return '\n'.join(str(person) for person in persons)
