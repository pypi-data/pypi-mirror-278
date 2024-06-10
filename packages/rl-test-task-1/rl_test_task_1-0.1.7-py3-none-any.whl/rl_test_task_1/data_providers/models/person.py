class Person:
    __id: int = 0

    __first_name: str = ''

    __last_name: str = ''

    def __init__(self, id: int, first_name: str, last_name: str) -> None:
        self.__id = id
        self.__first_name = first_name
        self.__last_name = last_name

    def __str__(self) -> str:
        return f'{self.__first_name} {self.__last_name} {self.__id}'

    @property
    def id(self) -> int:
        return self.__id
