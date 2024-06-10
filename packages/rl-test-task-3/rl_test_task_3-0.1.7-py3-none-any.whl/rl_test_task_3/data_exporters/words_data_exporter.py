from rl_test_common.common import Common
from rl_test_storage_handlers import StorageHandler
from rl_test_storage_handlers.file.params.file_data import FileData
from rl_test_storage_handlers.file.params.file_destination import \
    FileDestination
from rl_test_storage_handlers.params.storage_destination import \
    StorageDestination

from ..data_providers.data_parsers.output_data_parser import OutputDataParser
from ..data_providers.words_data_provider import WordsDataProvider
from .exceptions.unsupported_data_type import UnsupportedDataType
from .generic_data_exporter import GenericDataExporter


class WordsDataExporter(GenericDataExporter):
    __common: Common = Common()

    __output_data_parser: OutputDataParser = OutputDataParser()

    def __init__(self, storage_handler: StorageHandler, data_provider: WordsDataProvider) -> None:
        super().__init__(storage_handler, data_provider)

    def export(self, destination: StorageDestination) -> None:
        words: dict[int, str] = super()._data_provider.get()
        self.__export(destination, words)

    def __export(self, destination: StorageDestination, words: dict[int, str]) -> None:
        destination_type: str = self.__common.get_type(destination)

        sorted_words: dict[int, str] = self.__get_sorted_words(words)

        if destination_type is FileDestination.__name__:
            data: FileData = FileData(
                self.__output_data_parser.parse(sorted_words))
            super()._export(destination, data)

        else:
            raise UnsupportedDataType(destination_type)

    def __get_sorted_words(self, words: dict[int, str]) -> dict[int, str]:
        sorted_words: dict[int, str] = {}

        words_with_lexicographically_sorted_characters: dict[int,
                                                             str] = self.__get_words_with_lexicographically_sorted_characters(words)

        sorted_words_with_lexicographically_sorted_characters: dict[int, str] = self.__get_sorted_words_with_lexicographically_sorted_characters(
            words_with_lexicographically_sorted_characters)

        for key in sorted_words_with_lexicographically_sorted_characters:
            sorted_words[key] = words[key]

        return sorted_words

    def __get_words_with_lexicographically_sorted_characters(
            self,
            words: dict[int, str]) -> dict[int, str]:
        result: dict[int, str] = {}

        for key, value in words.items():
            result[key] = ''.join(sorted(value))

        return result

    def __get_sorted_words_with_lexicographically_sorted_characters(
            self,
            words_with_lexicographically_sorted_characters: dict[int, str]) -> dict[int, str]:
        return dict(sorted(
            words_with_lexicographically_sorted_characters.items(),
            key=lambda item: item[1]))
