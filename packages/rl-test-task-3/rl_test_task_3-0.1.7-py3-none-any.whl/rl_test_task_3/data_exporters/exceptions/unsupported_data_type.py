class UnsupportedDataType(Exception):
    def __init__(self, destination_type: str) -> None:
        message: str = f'There is no corresponding data type for {destination_type}.'
        super().__init__(message)
