class Input:
    __data: str = ''

    def __init__(self, data: str) -> None:
        self.__data = data

    @property
    def data(self) -> str:
        return self.__data
