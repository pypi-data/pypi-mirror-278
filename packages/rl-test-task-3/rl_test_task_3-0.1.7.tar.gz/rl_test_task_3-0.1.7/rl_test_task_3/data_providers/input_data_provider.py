from rl_test_storage_handlers.params.storage_data import StorageData
from rl_test_storage_handlers.params.storage_destination import \
    StorageDestination
from rl_test_storage_handlers.storage_handler import StorageHandler

from .data_provider import DataProvider
from .models import Input


class InputDataProvider(DataProvider):
    __input: Input = Input('')

    def __init__(self, storage_handler: StorageHandler, destination: StorageDestination) -> None:
        data: StorageData = storage_handler.read(destination)

        self.__input = Input(data.get())

    def get(self) -> Input:
        return self.__input
