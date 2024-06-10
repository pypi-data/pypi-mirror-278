import os

from dotenv import load_dotenv
from rl_test_common import Config
from rl_test_storage_handlers.file.params.file_destination import \
    FileDestination
from rl_test_storage_handlers.file.text_file_handler import TextFileHandler

from .data_exporters.words_data_exporter import WordsDataExporter
from .data_providers.input_data_provider import InputDataProvider
from .data_providers.words_data_provider import WordsDataProvider

load_dotenv()


class Client:
    __config: Config = Config(os.getenv('CONFIG_FILE_PATH'))

    __text_file_handler: TextFileHandler = TextFileHandler()

    def client_code(self):
        input_data_provider: InputDataProvider = self.__get_inputs_data_provider()

        words_data_provider: WordsDataProvider = WordsDataProvider(
            input_data_provider)

        words_data_exporter: WordsDataExporter = WordsDataExporter(
            self.__text_file_handler, words_data_provider)

        output_file_destination: FileDestination = FileDestination(
            self.__config.task_3_output_file_name)

        words_data_exporter.export(output_file_destination)

    def __get_inputs_data_provider(self) -> InputDataProvider:
        return InputDataProvider(
            self.__text_file_handler,
            FileDestination(self.__config.task_3_input_file_name))
