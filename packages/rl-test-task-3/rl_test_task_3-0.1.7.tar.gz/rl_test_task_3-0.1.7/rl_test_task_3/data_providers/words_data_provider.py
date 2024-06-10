from .data_parsers.input_data_parser import InputDataParser
from .data_provider import DataProvider
from .input_data_provider import InputDataProvider


class WordsDataProvider(DataProvider):
    __input_data_parser: InputDataParser = InputDataParser()

    __words: dict[int, str] = {}

    def __init__(self, input_data_provider: InputDataProvider) -> None:
        self.__words = self.__input_data_parser.get_parsed_data(
            input_data_provider.get())

    def get(self) -> dict[int, str]:
        return self.__words
