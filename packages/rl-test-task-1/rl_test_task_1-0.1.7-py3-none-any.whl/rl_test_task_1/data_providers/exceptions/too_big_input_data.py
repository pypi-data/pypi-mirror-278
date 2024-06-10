class TooBigInputData(Exception):
    def __init__(
            self,
            input_data_size_in_bytes: int,
            max_input_data_size_in_bytes: int) -> None:
        message: str = f'Input data size ({input_data_size_in_bytes} B) exceeds maximum input data size ({max_input_data_size_in_bytes} B).'
        super().__init__(message)
